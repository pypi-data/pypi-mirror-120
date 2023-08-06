from abc import ABC, abstractmethod

class View(ABC):

    @abstractmethod
    def create_view(self, master):
        """
        Where views are created
        """
        raise NotImplemented

    @abstractmethod
    def update_view(self, update_obj):
        """
        This is where you update you view with the data objec coming from the 
        model. Will Raise an error if not implemented
        """
        raise NotImplemented