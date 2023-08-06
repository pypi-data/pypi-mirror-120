import json
import os

HOME_PATH = os.path.realpath('..')
RESOURCES_PATH = HOME_PATH + '/resources'
MODELS_PATH = RESOURCES_PATH + '/models'
DATABASES_PATH = RESOURCES_PATH + '/databases'
SETTINGS = ''


def config_env(env='debug'):
    global SETTINGS
    env_dict = {'debug': 'Debug.json', 'release': 'Release.json'}
    with open(HOME_PATH + '/config/' + env_dict[env], 'r') as js:
        SETTINGS = json.load(js)
