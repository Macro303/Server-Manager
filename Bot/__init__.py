import logging
from pathlib import Path

import yaml

TOP_DIR = Path(__file__).resolve().parent.parent
LOGGER = logging.getLogger(__name__)


def save_config():
    with open(config_file, 'w', encoding='UTF-8') as yaml_file:
        yaml.safe_dump(CONFIG, yaml_file)


config_file = TOP_DIR.joinpath('config.yaml')
if config_file.exists():
    with open(config_file, 'r', encoding='UTF-8') as yaml_file:
        CONFIG = yaml.safe_load(yaml_file) or {
            'Prefix': '!',
            'Token': None,
            'Blacklist': []
        }
else:
    config_file.touch()
    CONFIG = {
        'Prefix': '!',
        'Token': None,
        'Blacklist': []
    }
save_config()
