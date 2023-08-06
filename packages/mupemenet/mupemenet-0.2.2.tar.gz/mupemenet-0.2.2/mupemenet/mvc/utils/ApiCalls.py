import json
from mupemenet.config.Config import Config
import mupemenet
from mupemenet.mvc.utils.Utils import measure, mupemenet_singleton
import urllib3
import concurrent.futures


@mupemenet_singleton
class ApiCall:

    def __init__(self) -> None:
        global BASE_URL
        global http_client
        BASE_URL = Config.SETTINGS['BASE_URL']
        headers = dict()
        headers['x-api-key'] =  Config.SETTINGS['API_KEY']
        http_client = urllib3.PoolManager(headers=headers, num_pools=2)

    @measure
    def GET(self, endpoint, succes, failure):
        
        try:
            url = BASE_URL + endpoint
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future_to_get = [executor.submit(http_client.request, 'GET', url)]
                for future in concurrent.futures.as_completed(future_to_get):
                    resp = future.result()
                    break
                status = resp.status
                if status != 200:
                    failure(ConnectionError("Erreur de connexion. Status: {}".format(status)))
                else:
                    data = json.loads(resp.data)
                    content = data['content']
                    succes(content)
        except Exception as e:
            failure(e) 


    def fetch_latest_embeddings(self, timestamp, success, failure):
        self.GET("/ai/latestembeddings/" + str(timestamp), success, failure)
