import re
import uuid
from pathlib import Path
from typing import List, Optional

import cv2
import numpy as np
from PIL import Image
from loguru import logger
from pdf2image import convert_from_path
from pyzbar.pyzbar import decode

from .database import Database
from .sql import *


class AtfHandler:
    template = re.compile(r'^ATF-([A-Z\d\*\-\%\$\.\/\+]+)-(\d+)$')

    def __init__(
            self,
            db: Database,
            create_user_id: int,
            create_user_name: str,
            mis_file_path: Path,
            unprocessed_folder: str,
            rotate_angle: int,
            rotate_count: int
    ):
        self.db = db
        self.create_user_id = create_user_id
        self.create_user_name = create_user_name
        self.mis_file_path = mis_file_path
        self.rotate_angle = rotate_angle
        self.rotate_count = rotate_count

        self.buffer: List[Image] = []
        self.doc_type: str = ''
        self.mkab_id: int = 0
        self.source_path: Optional[Path] = None
        self.unprocessed_folder = unprocessed_folder
        self.unprocessed_pages = []

    @property
    def unprocessed_path(self):
        _path = Path(self.source_path / self.unprocessed_folder)
        _path.mkdir(parents=True, exist_ok=True)
        return _path

    def _create_atf_record(self, filename: str):
        """
        Создание записи в МИС о прикреплённом файле

        :param filename:
        :return:
        """
        # Находим в настройках МИС, где должны лежать файлы для всеобщего обозрения
        try:
            unc_mis_files = self.db.select_one(GET_ATTACHMENT_PATH)[0]
        except (TypeError, KeyError):
            logger.error('Не найден параметр "Путь к хранилищу прикреплённых файлов" в таблице x_UserSettings')
            raise RuntimeError

        # Находим необходимый тип прикреплённых файлов
        try:
            file_type_id = self.db.select_one(GET_FILETYPE_ID, (self.doc_type,))[0]
        except (TypeError, KeyError):
            logger.error(f'Не найден тип прикрепляемого файла с кодом {self.doc_type}')
            raise RuntimeError

        # Находим идентификатор типа документа МКАБ
        desc_type_guid = self.db.select_one(GET_DOCUMENT_GUID)[0]

        # Получение МКАБ по идентификатору
        try:
            mkab = self.db.select_all(GET_MKAB, (self.mkab_id,), as_dict=True)[0]
        except IndexError:
            logger.error(f'МКАБ {self.mkab_id} не найден')
            raise RuntimeError

        # Добавляем информацию о файле
        cursor = self.db.execute_query(CREATE_FILEINFO, (file_type_id, desc_type_guid, mkab['UGUID']))
        file_info_id = cursor.lastrowid

        # Добавляем информацию о вложении
        self.db.execute_query(CREATE_ATTACHMENT, (
            self.create_user_id,
            self.create_user_name,
            file_info_id,
            '\\'.join((unc_mis_files, filename)),
            'Автоматически прикреплённый скан документа'
        ))
        logger.debug(f'В МКАБ {self.mkab_id} добавлен прикреплённый документ (FileInfoID={file_info_id})')

    def _create_dest_file(self, filename: str):
        """
        Создание файла PDF по пути, где хранятся файлы МИС
        :param filename:
        :return:
        """
        self.buffer[0].save(self.mis_file_path / filename, resolution=100.0, save_all=True, append_images=self.buffer[1:])
        logger.debug(f'Создан файл {self.mis_file_path / filename}')

    def _create_unprocessed_file(self, filename: str):
        """
        Создание файла PDF с необработанными страницами
        :param filename:
        :return:
        """
        self.unprocessed_pages[0].save(self.unprocessed_path / filename, resolution=100.0, save_all=True, append_images=self.unprocessed_pages[1:])
        logger.debug(f'Создан файл с необработанными страницами {self.unprocessed_path / filename}')

    def _purge(self):
        if len(self.buffer) > 0:
            self.source_path.mkdir(parents=True, exist_ok=True)
            filename = f'{uuid.uuid4()}.pdf'
            self._create_atf_record(filename)
            self._create_dest_file(filename)
            self.db.connection.commit()
            self.buffer = []
            self.doc_type = ''
            self.mkab_id = 0

    def _add_page(self, doc_type, mkab_id, page):
        if doc_type != self.doc_type or mkab_id != self.mkab_id:
            self._purge()
            self.doc_type = doc_type
            self.mkab_id = mkab_id

        self.buffer.append(page)

    @staticmethod
    def _rotate_image(image: np.ndarray, angle: int):
        logger.debug(f'Разворот страницы на {angle} градусов')
        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        rot_image = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
        return rot_image

    def decode(self, image: Image):
        result = decode(image)
        if len(result) > 0:
            return result

        # Если прямой подход не увенчался успехом, то пробуем
        # поворачивать страничку сначала влево, потом вправо
        for angle in (self.rotate_angle, -1 * self.rotate_angle):
            rot_image = np.asarray(image)
            rotation_iterations = 0
            while len(result) == 0 and rotation_iterations < self.rotate_count:
                rotation_iterations += 1
                rot_image = self._rotate_image(rot_image, angle)
                result = decode(rot_image)
                if len(result) > 0:
                    return result

        return result

    def process(self, file: Path) -> None:
        self.source_path = file.parent

        for page_index, page in enumerate(convert_from_path(file)):
            with logger.contextualize(filename=file.name, page=f'стр. № {page_index + 1}'):
                for barcode in self.decode(page):
                    logger.debug(f'Распознан ШК: "{barcode.data}"')
                    match = self.template.match(barcode.data.decode('utf-8'))
                    if match:
                        logger.info(f'ШК соответствует маске')
                        try:
                            self._add_page(match.group(1), match.group(2), page)
                        except RuntimeError:
                            ...
                        finally:
                            break
                    else:
                        logger.warning(f'ШК не соответствует маске')
                else:
                    self.unprocessed_pages.append(page)

        # По окончании обработки всех страниц документа очищаем буфер
        try:
            self._purge()
        except RuntimeError:
            # Но если что-то пошло не так, то помечаем весь документ как неспознанный,
            # чтобы не потерять данные
            self.unprocessed_pages = self.buffer

        # Если во время обработки файла были необработанные страницы,
        # то пишем об этом в лог и создаём файл с необработанными страницами в соответствующей папке
        if len(self.unprocessed_pages) > 0:
            logger.warning('Документ не обработан, либо обработан не полностью')
            self._create_unprocessed_file(file.name)
            self.unprocessed_pages = []
        else:
            logger.success('Документ успешно обработан')

        # Удаляем файл
        file.unlink()
