import logging
from pathlib import Path

import yaml

TOP_DIR = Path(__file__).resolve().parent.parent
LOGGER = logging.getLogger(__name__)


def save_config():
    validate_config()
    with open(config_file, 'w', encoding='UTF-8') as yaml_file:
        yaml.safe_dump(CONFIG, yaml_file)

def validate_config():
    if 'Prefix' not in CONFIG:
        CONFIG['Prefix'] = '!'
    if 'Token' not in CONFIG:
        CONFIG['Token'] = None
    if 'Moderator' not in CONFIG:
        CONFIG['Moderator'] = []
    if 'Blacklist' not in CONFIG:
        CONFIG['Blacklist'] = []


config_file = TOP_DIR.joinpath('config.yaml')
if config_file.exists():
    with open(config_file, 'r', encoding='UTF-8') as yaml_file:
        CONFIG = yaml.safe_load(yaml_file)
else:
    config_file.touch()
    CONFIG = {}
save_config()
