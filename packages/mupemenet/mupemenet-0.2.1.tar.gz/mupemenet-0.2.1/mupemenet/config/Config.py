import json
from mupemenet.mvc.utils.Utils import mupemenet_singleton
import pkg_resources
env_dict = {'debug': 'Debug.json', 'release': 'Release.json'}

@mupemenet_singleton
class Config:


    def __init__(self, env='debug') -> None:
        Config.HOME_PATH = pkg_resources.resource_filename('mupemenet', '')
        Config.RESOURCES_PATH = Config.HOME_PATH + '/resources'
        Config.MODELS_PATH = Config.RESOURCES_PATH + '/models'
        Config.ENV = env
        Config.DATABASES_PATH = "mupemenet/" + Config.ENV +'/databases'
        
        with open(Config.HOME_PATH + '/config/' + env_dict[env], 'r') as js:
            Config.SETTINGS = json.load(js)
    
    @staticmethod
    def get_env():
        return Config.ENV

    
    
