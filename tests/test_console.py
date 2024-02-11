#!/usr/bin/python3
"""
Tests for the console
"""
import sys
import unittest
from unittest.mock import patch
from console import HBnBCmd
from io import StringIO


class TestConsole(unittest.TestCase):
    def test_help(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("help show")
        self.assertEqual('Prints the string representation of an \
instance based on the class name and id.\n', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("help create")
        self.assertEqual('Creates a new instance of a given \
class, saves it (to the JSON file) and prints the id.\n', f.getvalue())

    def test_create(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("create BaseModel")
        self.assertIsInstance(f.getvalue(), str)
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("create")
        self.assertEqual(f.getvalue(), '** class name missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("create MyModel")
        self.assertEqual(f.getvalue(), '** class doesn\'t exist **\n')

    def test_show(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("show")
        self.assertEqual(f.getvalue(), '** class name missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("show MyModel")
        self.assertEqual(f.getvalue(), '** class doesn\'t exist **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("show BaseModel")
        self.assertEqual(f.getvalue(), '** instance id missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("show BaseModel 1111")
        self.assertEqual(f.getvalue(), '** no instance found **\n')

    def test_destroy(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("destroy")
        self.assertEqual(f.getvalue(), '** class name missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("destroy MyModel")
        self.assertEqual(f.getvalue(), '** class doesn\'t exist **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("destroy BaseModel")
        self.assertEqual(f.getvalue(), '** instance id missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("destroy BaseModel 1111")
        self.assertEqual(f.getvalue(), '** no instance found **\n')

    def test_all(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("all")
        self.assertIsInstance(f.getvalue(), str)
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("all BaseModel")
        self.assertIsInstance(f.getvalue(), str)
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("all MyModel")
        self.assertEqual(f.getvalue(), '** class doesn\'t exist **\n')

    def test_update(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("update")
        self.assertEqual(f.getvalue(), '** class name missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("update MyModel")
        self.assertEqual(f.getvalue(), '** class doesn\'t exist **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("update BaseModel")
        self.assertEqual(f.getvalue(), '** instance id missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("update BaseModel 1111")
        self.assertEqual(f.getvalue(), '** attribute name missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("create BaseModel")
        model_id = f.getvalue()
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"update BaseModel {model_id}")
        self.assertEqual(f.getvalue(), '** attribute name missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"update BaseModel {model_id} first")
        self.assertEqual(f.getvalue(), '** value missing **\n')

    def test_quit(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("quit")
        self.assertEqual(f.getvalue(), '')

    def test_EOF(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("EOF")
        self.assertEqual(f.getvalue(), '\n')

    def test_emptyline(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("")
        self.assertEqual(f.getvalue(), '')

    def test_basedoAll(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("BaseModel.all()")
        self.assertNotIn('[City]', f.getvalue())
        self.assertNotIn('[Review]', f.getvalue())
        self.assertNotIn('[Place]', f.getvalue())
        self.assertNotIn('[Amenity]', f.getvalue())
        self.assertNotIn('[State]', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("BaseModel.all")
        self.assertIn('**', f.getvalue())

    def test_reviewdoAll(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("Review.all()")
        self.assertNotIn('[BaseModel]', f.getvalue())
        self.assertNotIn('[User]', f.getvalue())
        self.assertNotIn('[State]', f.getvalue())
        self.assertNotIn('[Place]', f.getvalue())
        self.assertNotIn('[City]', f.getvalue())
        self.assertNotIn('[Amenity]', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("Review.all")
        self.assertIn('**', f.getvalue())

    def test_userdoAll(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmnd().onecmd("User.all()")
        self.assertNotIn('[BaseModel]', f.getvalue())
        self.assertNotIn('[City]', f.getvalue())
        self.assertNotIn('[Review]', f.getvalue())
        self.assertNotIn('[Place]', f.getvalue())
        self.assertNotIn('[Amenity]', f.getvalue())
        self.assertNotIn('[State]', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("User.all")
        self.assertIn('**', f.getvalue())

    def test_statedoAll(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("State.all()")
        self.assertNotIn('[BaseModel]', f.getvalue())
        self.assertNotIn('[City]', f.getvalue())
        self.assertNotIn('[Review]', f.getvalue())
        self.assertNotIn('[Place]', f.getvalue())
        self.assertNotIn('[Amenity]', f.getvalue())
        self.assertNotIn('[User]', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("State.all")
        self.assertIn('***', f.getvalue())

    def test_placedoAll(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("Place.all()")
        self.assertNotIn('[BaseModel]', f.getvalue())
        self.assertNotIn('[City]', f.getvalue())
        self.assertNotIn('[Review]', f.getvalue())
        self.assertNotIn('[State]', f.getvalue())
        self.assertNotIn('[Amenity]', f.getvalue())
        self.assertNotIn('[User]', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("Place.all")
        self.assertIn('**', f.getvalue())

    def test_amenitydoAll(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("Amenity.all()")
        self.assertNotIn('[BaseModel]', f.getvalue())
        self.assertNotIn('[City]', f.getvalue())
        self.assertNotIn('[Review]', f.getvalue())
        self.assertNotIn('[Place]', f.getvalue())
        self.assertNotIn('[State]', f.getvalue())
        self.assertNotIn('[User]', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("Amenity.all")
        self.assertIn('**', f.getvalue())

    def test_citydoAll(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("City.all()")
        self.assertNotIn('[BaseModel]', f.getvalue())
        self.assertNotIn('[State]', f.getvalue())
        self.assertNotIn('[Review]', f.getvalue())
        self.assertNotIn('[Place]', f.getvalue())
        self.assertNotIn('[Amenity]', f.getvalue())
        self.assertNotIn('[User]', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("City.all")
        self.assertIn('**', f.getvalue())

    def test_basedoCount(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("BaseModel.count()")
        self.assertIsInstance(int(f.getvalue().strip()), int)

    def test_userdoCount(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("User.count()")
        self.assertIsInstance(int(f.getvalue().strip()), int)

    def test_statedoCount(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("State.count()")
        self.assertIsInstance(int(f.getvalue().strip()), int)

    def test_placedoCount(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("Place.count()")
        self.assertIsInstance(int(f.getvalue().strip()), int)

    def test_citydoCount(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("City.count()")
        self.assertIsInstance(int(f.getvalue().strip()), int)

    def test_amenitydoCount(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("Amenity.count()")
        self.assertIsInstance(int(f.getvalue().strip()), int)

    def test_reviewdoCount(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("Review.count()")
        self.assertIsInstance(int(f.getvalue().strip()), int)

    def test_basedoShow(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("BaseModel.show()")
        self.assertEqual(f.getvalue(), '** instance id missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("create BaseModel")
        model_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"BaseModel.show({model_id})")
        self.assertIn('[BaseModel]', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"BaseModel.show(idf)")
        self.assertEqual(f.getvalue(), '** no instance found **\n')

    def test_userdoShow(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("User.show()")
        self.assertEqual(f.getvalue(), '** instance id missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("create User")
        model_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"User.show({model_id})")
        self.assertIn('[User]', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"User.show(idf)")
        self.assertEqual(f.getvalue(), '** no instance found **\n')

    def test_citydoShow(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("City.show()")
        self.assertEqual(f.getvalue(), '** instance id missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("create City")
        model_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"City.show({model_id})")
        self.assertIn('[City]', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"City.show(idf)")
        self.assertEqual(f.getvalue(), '** no instance found **\n')

    def test_statedoShow(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("State.show()")
        self.assertEqual(f.getvalue(), '** instance id missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("create State")
        model_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCmd().onecmd(f"State.show({model_id})")
        self.assertIn('[State]', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCmd().onecmd(f"State.show(idf)")
        self.assertEqual(f.getvalue(), '** no instance found **\n')

    def test_placedoShow(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("Place.show()")
        self.assertEqual(f.getvalue(), '** instance id missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("create Place")
        model_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Place.show({model_id})")
        self.assertIn('[Place]', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Place.show(idf)")
        self.assertEqual(f.getvalue(), '** no instance found **\n')

    def test_amenitydoShow(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("Amenity.show()")
        self.assertEqual(f.getvalue(), '** instance id missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("create Amenity")
        model_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Amenity.show({model_id})")
        self.assertIn('[Amenity]', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Amenity.show(idf)")
        self.assertEqual(f.getvalue(), '** no instance found **\n')

    def test_reviewdoShow(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("Review.show()")
        self.assertEqual(f.getvalue(), '** instance id missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("create Review")
        model_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Review.show({model_id})")
        self.assertIn('[Review]', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Review.show(idf)")
        self.assertEqual(f.getvalue(), '** no instance found **\n')

    def test_reviewdoDestroy(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("Review.destroy()")
        self.assertEqual(f.getvalue(), '** instance id missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("create Review")
        model_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Review.destroy({model_id})")
        self.assertEqual(f.getvalue(), '')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Review.show({model_id})")
        self.assertEqual(f.getvalue(), '** no instance found **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Review.destroy(idf)")
        self.assertEqual(f.getvalue(), '** no instance found **\n')

    def test_basedoDestroy(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("BaseModel.destroy()")
        self.assertEqual(f.getvalue(), '** instance id missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("create BaseModel")
        model_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"BaseModel.destroy({model_id})")
        self.assertEqual(f.getvalue(), '')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"BaseModel.show({model_id})")
        self.assertEqual(f.getvalue(), '** no instance found **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"BaseModel.destroy(idf)")
        self.assertEqual(f.getvalue(), '** no instance found **\n')

    def test_userdoDestroy(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("User.destroy()")
        self.assertEqual(f.getvalue(), '** instance id missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("create User")
        model_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"User.destroy({model_id})")
        self.assertEqual(f.getvalue(), '')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"User.show({model_id})")
        self.assertEqual(f.getvalue(), '** no instance found **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"User.destroy(idf)")
        self.assertEqual(f.getvalue(), '** no instance found **\n')

    def test_placedoDestroy(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("Place.destroy()")
        self.assertEqual(f.getvalue(), '** instance id missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("create Place")
        model_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Place.destroy({model_id})")
        self.assertEqual(f.getvalue(), '')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Place.show({model_id})")
        self.assertEqual(f.getvalue(), '** no instance found **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Place.destroy(idf)")
        self.assertEqual(f.getvalue(), '** no instance found **\n')

    def test_statedoDestroy(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("State.destroy()")
        self.assertEqual(f.getvalue(), '** instance id missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("create State")
        model_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"State.destroy({model_id})")
        self.assertEqual(f.getvalue(), '')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"State.show({model_id})")
        self.assertEqual(f.getvalue(), '** no instance found **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"State.destroy(idf)")
        self.assertEqual(f.getvalue(), '** no instance found **\n')

    def test_citydoDestroy(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("City.destroy()")
        self.assertEqual(f.getvalue(), '** instance id missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("create City")
        model_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"City.destroy({model_id})")
        self.assertEqual(f.getvalue(), '')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"City.show({model_id})")
        self.assertEqual(f.getvalue(), '** no instance found **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"City.destroy(idf)")
        self.assertEqual(f.getvalue(), '** no instance found **\n')

    def test_amenitydoDestroy(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("Amenity.destroy()")
        self.assertEqual(f.getvalue(), '** instance id missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("create Amenity")
        model_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Amenity.destroy({model_id})")
        self.assertEqual(f.getvalue(), '')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Amenity.show({model_id})")
        self.assertEqual(f.getvalue(), '** no instance found **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCmd().onecmd(f"Amenity.destroy(idf)")
        self.assertEqual(f.getvalue(), '** no instance found **\n')

    def test_basedoUpdate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("BaseModel.update()")
        self.assertEqual(f.getvalue(), '** instance id missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("BaseModel.update(1111)")
        self.assertEqual(f.getvalue(), '** attribute name missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("create BaseModel")
        model_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"BaseModel.update({model_id})")
        self.assertEqual(f.getvalue(), '** attribute name missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"BaseModel.update({model_id}, first)")
        self.assertEqual(f.getvalue(), '** value missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"BaseModel.update({model_id}, first, 3)")
        self.assertEqual(f.getvalue(), '')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"BaseModel.show({model_id})")
        self.assertIn('first', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"BaseModel.update({model_id},\
{{'second': 5, 'third': three}})")
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"BaseModel.show({model_id})")
        self.assertIn('third', f.getvalue())
        self.assertIn('second', f.getvalue())

    def test_userdoUpdate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("User.update()")
        self.assertEqual(f.getvalue(), '** instance id missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("User.update(1111)")
        self.assertEqual(f.getvalue(), '** attribute name missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("create User")
        model_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"User.update({model_id})")
        self.assertEqual(f.getvalue(), '** attribute name missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"User.update({model_id}, first)")
        self.assertEqual(f.getvalue(), '** value missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"User.update({model_id}, first, 3)")
        self.assertEqual(f.getvalue(), '')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"User.show({model_id})")
        self.assertIn('first', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"User.update({model_id},\
{{'second': 5, 'third': three}})")
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"User.show({model_id})")
        self.assertIn('third', f.getvalue())
        self.assertIn('second', f.getvalue())

    def test_placedoUpdate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("Place.update()")
        self.assertEqual(f.getvalue(), '** instance id missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("Place.update(1111)")
        self.assertEqual(f.getvalue(), '** attribute name missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("create Place")
        model_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Place.update({model_id})")
        self.assertEqual(f.getvalue(), '** attribute name missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Place.update({model_id}, first)")
        self.assertEqual(f.getvalue(), '** value missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Place.update({model_id}, first, 3)")
        self.assertEqual(f.getvalue(), '')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Place.show({model_id})")
        self.assertIn('first', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Place.update({model_id},\
{{'second': 5, 'third': three}})")
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Place.show({model_id})")
        self.assertIn('third', f.getvalue())
        self.assertIn('second', f.getvalue())

    def test_statedoUpdate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("State.update()")
        self.assertEqual(f.getvalue(), '** instance id missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("State.update(1111)")
        self.assertEqual(f.getvalue(), '** attribute name missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("create State")
        model_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"State.update({model_id})")
        self.assertEqual(f.getvalue(), '** attribute name missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"State.update({model_id}, first)")
        self.assertEqual(f.getvalue(), '** value missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"State.update({model_id}, first, 3)")
        self.assertEqual(f.getvalue(), '')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"State.show({model_id})")
        self.assertIn('first', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"State.update({model_id},\
{{'second': 5, 'third': three}})")
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"State.show({model_id})")
        self.assertIn('third', f.getvalue())
        self.assertIn('second', f.getvalue())

    def test_citydoUpdate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("City.update()")
        self.assertEqual(f.getvalue(), '** instance id missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("City.update(1111)")
        self.assertEqual(f.getvalue(), '** attribute name missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("create City")
        model_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"City.update({model_id})")
        self.assertEqual(f.getvalue(), '** attribute name missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"City.update({model_id}, first)")
        self.assertEqual(f.getvalue(), '** value missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"City.update({model_id}, first, 3)")
        self.assertEqual(f.getvalue(), '')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"City.show({model_id})")
        self.assertIn('first', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"City.update({model_id},\
{{'second': 5, 'third': three}})")
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"City.show({model_id})")
        self.assertIn('third', f.getvalue())
        self.assertIn('second', f.getvalue())

    def test_amenitydoUpdate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("Amenity.update()")
        self.assertEqual(f.getvalue(), '** instance id missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("Amenity.update(1111)")
        self.assertEqual(f.getvalue(), '** attribute name missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("create Amenity")
        model_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Amenity.update({model_id})")
        self.assertEqual(f.getvalue(), '** attribute name missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Amenity.update({model_id}, first)")
        self.assertEqual(f.getvalue(), '** value missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Amenity.update({model_id}, first, 3)")
        self.assertEqual(f.getvalue(), '')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Amenity.show({model_id})")
        self.assertIn('first', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Amenity.update({model_id},\
{{'second': 5, 'third': three}})")
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Amenity.show({model_id})")
        self.assertIn('third', f.getvalue())
        self.assertIn('second', f.getvalue())

    def test_reviewdoUpdate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("Review.update()")
        self.assertEqual(f.getvalue(), '** instance id missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("Review.update(1111)")
        self.assertEqual(f.getvalue(), '** attribute name missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd("create Review")
        model_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Review.update({model_id})")
        self.assertEqual(f.getvalue(), '** attribute name missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Review.update({model_id}, first)")
        self.assertEqual(f.getvalue(), '** value missing **\n')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Review.update({model_id}, first, 3)")
        self.assertEqual(f.getvalue(), '')
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Review.show({model_id})")
        self.assertIn('first', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Review.update({model_id},\
{{'second': 5, 'third': three}})")
        with patch('sys.stdout', new=StringIO()) as f:
            HBnBCmd().onecmd(f"Review.show({model_id})")
        self.assertIn('third', f.getvalue())
        self.assertIn('second', f.getvalue())
