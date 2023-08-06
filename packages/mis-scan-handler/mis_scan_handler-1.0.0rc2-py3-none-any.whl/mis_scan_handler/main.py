from pathlib import Path

import typer
from loguru import logger

from .handlers import AtfHandler, Database
from . import __version__

LOGGER_SETTINGS = {
    'rotation'   : '00:00',
    'retention'  : '3 weeks',
    'compression': 'zip',
    'format'     : '{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {extra[filename]: <50} | {extra[page]: <10} | {message}'
}

TYPER_OPTIONS = {
    'unprocessed_folder': {
        'default': 'UNPROCESSED',
        'envvar' : 'MHS_UNPROCESSED_FOLDER',
        'help'   : 'Наименование папки, куда перемещаются документы с ошибками обработки'
    },
    'create_user_id'    : {
        'default': 1,
        'envvar' : 'MSH_CREATE_USER_ID',
        'help'   : 'Идентификатор пользователя, прикрепившего файл'
    },
    'create_user_name'  : {
        'default': 'Администратор',
        'envvar' : 'MSH_CREATE_USER_NAME',
        'help'   : 'ФИО пользователя, прикрепившего файл'
    },
    'mis_db_server'     : {
        'default': ...,
        'envvar' : 'MIS_DB_SERVER',
        'help'   : 'Адрес сервера СУБД МИС'
    },
    'mis_db_port'       : {
        'default': 1433,
        'envvar' : 'MIS_DB_PORT',
        'help'   : 'Порт сервера СУБД МИС'
    },
    'mis_db_name'       : {
        'default': ...,
        'envvar' : 'MIS_DB_NAME',
        'help'   : 'Наименование БД МИС'
    },
    'mis_db_username'   : {
        'default': 'sa',
        'envvar' : 'MIS_DB_USERNAME',
        'help'   : 'Имя пользователя для подключения к БД МИС'
    },
    'mis_db_password'   : {
        'default': ...,
        'envvar' : 'MIS_DB_PASSWORD',
        'help'   : 'Пароль пользователя для подключения к БД МИС'
    },
    'mis_file_path'     : {
        'default': ...,
        'envvar' : 'MIS_FILE_PATH',
        'help'   : 'Путь до хранилища прикреплённых файлов МИС'
    },
    'rotate_angle'      : {
        'default': 5,
        'envvar' : 'ROTATE_ANGLE',
        'help'   : 'Угол поворота страницы при попытке распознавания'
    },
    'rotate_count'      : {
        'default': 7,
        'envvar' : 'ROTATE_COUNT',
        'help'   : 'Количество итераций попыток распознавания ШК поворотом страницы'
    }
}

app = typer.Typer()


def version_callback(value: bool):
    if value:
        typer.echo(f"MIS Scan Handler version: {__version__}")
        raise typer.Exit()


# noinspection PyUnusedLocal
@app.command()
def main(
        source_path: Path,
        unprocessed_folder: str = typer.Option(**TYPER_OPTIONS['unprocessed_folder']),
        create_user_id: int = typer.Option(**TYPER_OPTIONS['create_user_id']),
        create_user_name: str = typer.Option(**TYPER_OPTIONS['create_user_name']),
        mis_db_server: str = typer.Option(**TYPER_OPTIONS['mis_db_server']),
        mis_db_port: int = typer.Option(**TYPER_OPTIONS['mis_db_port']),
        mis_db_name: str = typer.Option(**TYPER_OPTIONS['mis_db_name']),
        mis_db_username: str = typer.Option(**TYPER_OPTIONS['mis_db_username']),
        mis_db_password: str = typer.Option(**TYPER_OPTIONS['mis_db_password']),
        mis_file_path: Path = typer.Option(**TYPER_OPTIONS['mis_file_path']),
        rotate_angle: int = typer.Option(**TYPER_OPTIONS['rotate_angle']),
        rotate_count: int = typer.Option(**TYPER_OPTIONS['rotate_count']),

        version: bool = typer.Option(None, '--version', callback=version_callback, is_eager=True)
):
    # Инициализируем подключение к БД и обработчик
    db = Database(mis_db_server, mis_db_port, mis_db_name, mis_db_username, mis_db_password)
    handler = AtfHandler(db, create_user_id, create_user_name, mis_file_path, unprocessed_folder, rotate_angle, rotate_count)

    # Добавляем журнал приложения по пути исполнения
    logger.add(source_path / 'logs' / 'debug.log', **LOGGER_SETTINGS)

    # Проходим по каждому PDF-файлу
    for file in source_path.glob('*.pdf'):
        with logger.contextualize(filename=file.name, page=''):
            handler.process(file)


if __name__ == '__main__':
    app()
