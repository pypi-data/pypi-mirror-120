import os

USER_HOME = os.path.expanduser('~')
BULLETIN_DIR = os.path.join(USER_HOME, '.bulletin')
CONFIG_DIR = os.path.join(BULLETIN_DIR, 'querybulletin')
if not os.path.isdir(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)

CONFIG_PATH = os.path.join(CONFIG_DIR, 'config.json')

DEFAULT_COLUMNS = [
    'eventid',
    'eventdate',
    'duration',
    'eventtype',
    'last_modified',
]

CSV_DELIMITER = '|'
