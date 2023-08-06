from mupemenet.config.Config import Config
import os
import cv2
import numpy as np
from mupemenet.facenet.Facenet import Facenet
from mupemenet.mvc.utils.Utils import measure, mupemenet_singleton, synchronized
from typing import Union
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
import json
import ast
from logging import debug, info

USER_INFO = 'user_info'
USER_DATA = 'user_data'
LATEST_ID = 'latest_id'
LATEST_TIMESTAMP = 'latest_timestamp'


def scope_db(func):
    def decorator(*args, **kwargs):
        global db

        filename = Config.DATABASES_PATH + '/users.json'
        storage = CachingMiddleware(JSONStorage)
        os.makedirs(Config.DATABASES_PATH, exist_ok = True)
        with TinyDB(filename, storage=storage, indent=4) as db:
            return func(*args, **kwargs)

    return decorator


@mupemenet_singleton
class UserDB:

    @scope_db
    def get_user_by_id(self, id):
        result = db.table(USER_INFO).get(Query().id == id)
        return result if result else  {
            "matricule": "",
            "name": "------",
            "id": -1
        }
    
    

    @scope_db
    def __get_latest_id__(self):
        result = db.table(LATEST_ID).search(Query().tag == 'latest')
        return result[0]['id'] if result else -1

    @scope_db
    def __set_latest_id__(self, id):
        db.table(LATEST_ID).upsert(
            {'tag': 'latest', 'id': id},
            Query().tag == 'latest')

    def __get_user_id_by_matricule__(self, matricule):
        user = self.get_user_by_matricule(matricule)
        return user['id'] if user is not None else -1

    @scope_db
    @measure
    def __upsert_user_data__(self, data):
        db.table(USER_DATA).upsert(data,
                                   Query().matricule == data['matricule'])

    @scope_db
    def __upsert_user_info__(self, info):
        db.table(USER_INFO).upsert(info, Query().matricule == info['matricule'])

    @scope_db
    def get_user_by_matricule(self, matricule):
        result = db.table(USER_INFO).search(Query().matricule == matricule)
        return result[0] if result else None

    @synchronized
    @measure
    def upsert(self, inp: Union[list, dict]):
        lst = list()
        if isinstance(inp, list):
            lst = inp
        elif isinstance(inp, dict):
            lst.append(inp)
        else:
            raise ValueError("Argument should be either a list or a dictionnary")
        for data in lst:
            self.__upsert_user_data__(data)
            id = self.__get_user_id_by_matricule__(data['matricule'])
            new_id = id if id >= 0 else self.__get_latest_id__() + 1
            user = {
                'matricule': data['matricule'],
                'name': data['name'], 'id': new_id
            }
            self.__upsert_user_info__(user)
            self.__set_latest_id__(new_id)
        if len(lst) > 0:
            self.build_fr_model()

    def load_user_data_from_file(self, filename):
        with open(filename) as json_file:
            data = json.load(json_file)
            return data

    def get_embeddings_from_data(self, data):
        embeds = "[{}]".format(data['embeds'])
        embeds = ast.literal_eval(embeds)
        return embeds

    @scope_db
    def get_embeddings_from_matricule(self, matricule):
        data = db.table(USER_DATA).get(Query().matricule == matricule)
        if data:
            return self.get_embeddings_from_data(data)
        else:
            raise RuntimeError("Could not retrieve data from matricule {}".format(matricule))

    @scope_db
    def get_latest_timestamp(self):
        result = db.table(LATEST_TIMESTAMP).get(Query().tag == 'latest')
        return result['timestamp'] if result else 0

    @scope_db
    def set_latest_timestamp(self, timestamp):
        db.table(LATEST_TIMESTAMP).upsert(
            {'tag': 'latest', 'timestamp': timestamp},
            Query().tag == 'latest')

    @scope_db
    def count_users(self):
        return db.table(USER_INFO).__len__()

    @scope_db
    @measure
    def build_fr_model(self):
        features = None
        responses = None
        users = db.table(USER_INFO).all()
        # Read embeddings into memory
        for user in users:
            id = user['id']
            matricule = user['matricule']
            embeds = np.array(self.get_embeddings_from_matricule(matricule))
            embeds = Facenet.normalize(embeds)
            features = embeds if features is None else np.vstack([features, embeds])
            resp = np.array([id for _id_ in range(len(embeds))])
            responses = resp if responses is None else np.hstack([responses, resp])

        model = cv2.ml.KNearest_create()
        model.setDefaultK(5)
        model.train(np.float32(features), cv2.ml.ROW_SAMPLE, np.int32(responses))
        filename = Config.MODELS_PATH + "/faces.xml"
        model.save(filename)

        return True
