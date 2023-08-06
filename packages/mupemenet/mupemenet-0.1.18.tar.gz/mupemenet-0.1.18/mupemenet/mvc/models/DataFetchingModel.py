from datetime import datetime
from logging import debug, error
import time
from mupemenet.mvc.utils.ApiCalls import ApiCall
from mupemenet.userdb.UserDB import UserDB
from mupemenet.mvc.models.Model import Model
import json


class DataFetchingModel(Model):

    def __init__(self) -> None:
        super().__init__()
        self.db = UserDB()
        self.api = ApiCall()
  
    def update_model(self, update_obj):

        def on_success(content):
            debug("Dataset loading done!")

            def transform(item):
                # Convert the data to proper json as it comes as byte buffer
                transformed_item = json.loads(
                    "".join([chr(i) for i in item['data']['data']])
                )
                return transformed_item

            if len(content) > 0:
                sorted(content,
                       key=lambda item: item['retrieval_timestamp'],
                       reverse=True
                       )
                timestamp = round(time.time() * 1000)
                self.db.set_latest_timestamp(timestamp) #content[0]['retrieval_timestamp']
                content = [transform(item) for item in content]
                self.db.upsert(content)

            message = "Téléchargement terminé"
            update_obj = {"message_color": 'green', "message": message}
            if len(content) <= 0:
                debug("User database is up-to-date")
            else:
                debug("Fetched users")
                for item in content:
                    debug("|     {}".format(item['name']))
            self.update_listener(update_obj)
            
            
        def on_failure(failure):
            error_message = "Verifiez votre connexion internet"
            error("{}".format(failure))
            update_obj = {"message_color": 'red', "message": error_message}
            self.update_listener(update_obj)
                

        def time_since_last_update(timestamp):
            date1 = datetime.fromtimestamp(timestamp/1000)
            date2 = datetime.now()
            delta = date2-date1
            return delta.days

        timestamp = self.db.get_latest_timestamp()
        la = time_since_last_update(timestamp)
        if la>30:
            debug(f"It has been {la} days since last update. Updating database...")
            self.api.fetch_latest_embeddings(
                timestamp=timestamp,
                success=on_success,
                failure=on_failure
            )
        else:
            debug(f"Database update time is not yet. It's only been {la} days since last update")
            message = "Téléchargement terminé"
            update_obj = {"message_color": 'green', "message": message}
            self.update_listener(update_obj)
