import configparser

config = configparser.ConfigParser()
config.read('settings.ini')

MAIN_CONFIG = config['main']
