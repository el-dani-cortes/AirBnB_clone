#!/usr/bin/python3
"""Module base_model
"""
import uuid
import datetime


class BaseModel:
    """
    Class that defines all common attributes/methods for other classes
    """
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

    def __str__(self):
        """Method that override the str method and returns a specific string

        Args:
           No arguments.

        Return:
           Specific format string with class name, id and dict atributtes
           of the object.

        """
        return ("[<{}>] (<{}>) <{}>".format(__class__.__name__, self.id,
                                            self.__dict__))

    def save(self):
        """
        Method that updated the date and time of a BaseModel object
        """
        self.updated_at = datetime.datetime.now()

    def to_dict(self):
        """Method that returns a dictionary containing all keys/values of
           __dict__ of the instance.

        Args:
           No arguments.

        Return:
           A dictionary containing all keys/values
           of __dict__ of the object

        """
        dict_attrs = {}
        for key in self.__dict__.keys():
            if key == "created_at" or key == "updated_at":
                value = getattr(self, key).isoformat()
                dict_attrs[key] = value
            else:
                dict_attrs[key] = getattr(self, key)
        dict_attrs["__class__"] = __class__.__name__
        return dict_attrs
