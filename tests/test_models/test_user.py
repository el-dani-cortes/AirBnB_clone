#!/usr/bin/python3
"""Unittest for base_model.py file
"""
import unittest
import unittest.mock 
from models.base_model import BaseModel
from models.user import User
import os
import uuid
import datetime
from models.engine.file_storage import FileStorage
import io


class Test_User_model(unittest.TestCase):
    """
    Defines a class to evaluate diferent test cases for base_model.py file
    """

    def setUp(self):
        """set environment to start testing"""
        # Empty objects in engine
        from models.engine.file_storage import FileStorage
        # Remove file.json if exists
        if os.path.exists("file.json"):
            os.remove("file.json")

    def tearDown(self):
        """set enviroment when testing is finished"""
        # Empty objects in engine
        FileStorage._FileStorage__objects = {}
        # Remove file.json if exists
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_instance_type_id_class(self):
        """
        Checks for a instance of the class
        """
        model = User()
        self.assertIsInstance(model, User)
        self.assertIsInstance(model, BaseModel)
        self.assertFalse(type(model) == type(User))
        self.assertFalse(id(model) == id(User))
        model_2 = User()
        self.assertTrue(type(model) == type(model_2))
        self.assertFalse(id(model) == id(model_2))

    def test_instances_attributes(self):
        """
        Checks attributes created to the new object
        """
        # Checks that base attributes are created for the object
        model = User()
        my_attrs = ['id', 'created_at', 'updated_at']
        for attr in my_attrs:
            self.assertEqual(attr in model.__dict__.keys(), True)

        # Checks that some falses attributes
        my_attrs = ['name', 'create_time', 'update_time']
        for attr in my_attrs:
            self.assertEqual(attr in model.__dict__.keys(), False)

    def test_unique_id(self):
        """
        Checks for a unique id
        """
        # Checks if two instances has diferents id
        model = User()
        model_2 = User()
        self.assertNotEqual(model.id, model_2.id)

    def test_datetime(self):
        """
        Checks for datetime attributes
        """
        # Test if two instnace has diferent datetime
        model = User()
        model_2 = User()
        self.assertNotEqual(model.created_at, model_2.created_at)
        self.assertNotEqual(model.updated_at, model_2.updated_at)

        # Test if attribute created_at and updated_at are datetime instance
        model = User()
        self.assertIsInstance(model.created_at, datetime.datetime)
        self.assertIsInstance(model.updated_at, datetime.datetime)

    def test_UUID4(self):
        """
        Checks for the ID generation protocol
        """
        # Checks that the ID generated is the version 4
        model = User()
        version = uuid.UUID(model.id).version
        self.assertEqual(version, 4)

    def test_created_and_updated_at(self):
        """
        Checks if updated_t attribute changes when a new attribute is
        added to the object and created_at is the same all the time.
        """
        # Checks that updated_at changes
        model = User()
        updated_1 = str(model.updated_at)
        model.name = "Betty"
        model.save()
        updated_2 = str(model.updated_at)
        self.assertNotEqual(updated_1, updated_2)

        # Checks that created_at doesn't change
        model = User()
        created_1 = str(model.created_at)
        model.last_name = "Holberton"
        model.save()
        created_2 = str(model.created_at)
        self.assertEqual(created_1, created_2)

    def test_add_new_attributes(self):
        """
        Checks that can add new attributes to the objects
        """
        # Checks new attributes are added
        dict_attr = {'first_name': 'Betty',
                     'last_name': 'Holberton', 'age': 40,
                     'email': 'wisvem@hotmail.com', 'password': "980336"}
        model = User()
        for key, value in dict_attr.items():
            setattr(model, key, value)
        for key, value in dict_attr.items():
            self.assertTrue(hasattr(model, key))
            self.assertEqual(getattr(model, key), value)

        # Checks for all attributes for the object
        my_attrs = ['id', 'created_at', 'updated_at', 'email', 'password',
                    'first_name', 'last_name', 'age']
        for attr in my_attrs:
            self.assertEqual(attr in model.__dict__.keys(), True)

    def test_str_method(self):
        """
        Checks str method
        """
        model = User()
        string = "[{}] ({}) {}".format(model.__class__.__name__, model.id,
                                       model.__dict__)
        self.assertEqual(str(model), string)

    def test_to_dict_method(self):
        """
        Checks dict method
        """
        # Checks if it convert to a dict type
        model = User()
        model.name = "Holberton"
        model.my_number = 89
        model.my_float = 100.54
        model.my_list = ["Hello", "world", 100]
        model.my_dict = {'name': 'Betty', 'last_name': 'Holberton', 'age': 85}
        model.save()
        model_json = model.to_dict()
        # checks if the method really convert to a dict type all the attributes
        self.assertEqual(type(model_json), dict)
        for key, value in model_json.items():
            # checks if the dict has the same attributes keys that the object
            self.assertTrue(hasattr(model, key))
            # checks if datetime was safe as a iso format and its type
            if key == "created_at" or key == "updated_at":
                _datetime = getattr(model, key).isoformat()
                self.assertEqual(_datetime, value)
                self.assertTrue(type(value) == str)
            # checks the class name attribute and its type
            elif key == "__class__":
                self.assertEqual(model.__class__.__name__, value)
                self.assertTrue(type(value) == str)
            else:
                # checks the value for others attributes
                self.assertEqual(getattr(model, key), value)
                # Checks the types and formats of the attributes
                if key == "id":
                    version = uuid.UUID(value).version
                    self.assertEqual(version, 4)
                    self.assertTrue(type(value), str)
                elif key == "name":
                    self.assertTrue(type(value) == str)
                elif key == "my_number":
                    self.assertTrue(type(value) == int)
                elif key == "my_list":
                    self.assertTrue(type(value) == list)
                elif key == "my_float":
                    self.assertTrue(type(value) == float)
                elif key == "my_dict":
                    self.assertTrue(type(value) == dict)

    def test_init_User_from_dictionary(self):
        """
        Checks when it is passed a dictionary to the init method.
        """
        model = User()
        model.name = "Holberton"
        model.my_number = 89
        model_json = model.to_dict()
        my_new_model = User(**model_json)
        # Checks that the object has the same attributes that the model
        dict_attr = {'name': 'Holberton', 'my_number': 89, 'id': model.id,
                     'created_at': model.created_at,
                     'updated_at': model.updated_at}
        for key, value in dict_attr.items():
            self.assertTrue(hasattr(my_new_model, key))
            self.assertEqual(getattr(my_new_model, key), value)
        # Checks if __class__ attribute was not added
        self.assertTrue(hasattr(my_new_model, key))
        cls_name = getattr(my_new_model, key)
        self.assertNotEqual(cls_name, model_json["__class__"])

    def test_instance_kwargs(self):
        """Checks if user with args is instance of base_model"""
        d = {"name": "Holberton"}
        b = User(**d)
        self.assertTrue(isinstance(b, BaseModel))

    # def test_classattr(self):
    #     """Check class default attributes"""
    #     my_model = User()
    #     attrlist = ["email", "password", "first_name", "last_name"]
    #     mydict = my_model.__dict__
    #     for i in attrlist:
    #         self.assertFalse(i in mydict)
    #         self.assertTrue(hasattr(mydict, i))
    #         self.assertEqual(getattr(mydict, i, False), "")

    def test_print(self):
        """ Tests the __str__ method """
        b1 = User()
        s = "[{:s}] ({:s}) {:s}\n"
        s = s.format(b1.__class__.__name__, b1.id, str(b1.__dict__))
        with unittest.mock.patch('sys.stdout', new=io.StringIO()) as p:
            print(b1)
            st = p.getvalue()
            self.assertEqual(st, s)
