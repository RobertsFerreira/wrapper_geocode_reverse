import logging
from pathlib import Path


def configure_log():
    path_log = '.\\data\\log'

    path = Path(path_log)

    if not path.exists():
        path.mkdir(parents=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename=f'{path_log}\\wrapper_geocode.log',
        filemode='a',
    )

    return logging


logger = configure_log()
