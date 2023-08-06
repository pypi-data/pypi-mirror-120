from abc import ABC, abstractmethod
from mupemenet.mvc.exceptions.Customexceptions import ModelNotInitializedError, ModelUpdateNotImplementedError

class Model(ABC):
    
    @abstractmethod
    def update_model(self, update_obj):
        """
        This is where you manipulate your model. i.e network call,
        database update, etc. The result should be returned like this:
        self.update_listener(result_object)
        """
        raise ModelUpdateNotImplementedError()

    def set_update_listener(self, update_listener):
        self.update_listener = update_listener
    
    def get_update_listener(self):
        return self.update_listener
