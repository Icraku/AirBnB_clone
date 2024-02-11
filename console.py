#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

def parse_arguments(arg_string):
    brackets = re.search(r"\[(.*?)\]", arg_string)
    curlyBraces = re.search(r"\{(.*?)\}", arg_string)
    if curlyBraces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg_string)]
        else:
            tkn_list = split(arg_string[:brackets.span()[0]])
            ret_list = [i.strip(",") for i in tkn_list]
            ret_list.append(brackets.group())
            return ret_list
    else:
        tkn_list = split(arg_string[:curlyBraces.span()[0]])
        ret_list = [i.strip(",") for i in tkn_list]
        ret_list.append(curlyBraces.group())
        return ret_list

class HBNBConsole(cmd.Cmd):
    """Used to define the HBnB cmd interpreter.
    Attributes: prompt (string): The cmd prompt."""
    cmd_prompt = "(HBnB) "
    available_classes = {
            "BaseModel",
            "State",
            "Review",
            "Place",
            "User",
            "Amenity",
            "City"
            }
    def eofCmd(self, argument):
        """EOF signals the exit the program."""
        print("")
        return True

    def quitCmd(self, argument):
        """Quit command exits the program."""
        return True

    def blankLine(self):
        """Do nothing when blank line is received."""
        pass

    def defaultCmd(self, argument):
        """Default behaviour when input is inavlid."""
        cmd_dict = {
                "show": self.do_show,
                "update": self.do_update,
                "destroy": self.do_destroy,
                "count": self.do_count,
                "all": self.do_show_all
                }
        matched = re.search(r"\.", argument)
        if matched is not None:
            arg_list = [argument[:match.span()[0]], argument[match.span()[1]:]]
            matched = re.search(r"\((.*?)\)", arg_list[1])
            if matched is not None:
                cMd = [arg_list[1][:match.span()[0]], match.group()[1:-1]]
                if cMd[0] in cmd_dict.keys():
                    call = "{} {}".format(arg_list[0], cMd[1])
                    return cMd_dict[cMd[0]](call)
                print("*** Unknown syntax: {}".format(argument))
                return False

    def createInst(self, argument):
        """To create a new class instance and print the instance ID
        Usage: create <class>"""
        arg_list = parse_arguments(argument)
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBConsole.available_classes:
            print("** class doesn't exist **")
        else:
            print(eval(arg_list[0])().id)
            storage.save()

    def showInst(self, argument):
        """To display the string rep of a class instance of a given id.
        Usage: show <class> <id> or <class>.show(<id>)"""
        obj_dict = storage.all()
        arg_list = parse_arguments(argument)
        if len(arg_list) == 0:
            print("** class name missing **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        elif arg_list[0] not in HBNBConsole.available_classes:
            print("** class doesn't exist **")
        elif "{}.{}".format(arg_list[0], arg_list[1]) not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict["{}.{}".format(arg_list[0], arg_list[1])])

    def showAll(self, argument):
        """To display string rep of all instances of a given class but if
        none is given, it displays all instantiated objects.
        Usage: <class>.all() or all <class> or all """
        arg_list = parse_arguments(argument)
        if len(arg_list) > 0 and arg_list[0] not in HBnBCommand.available_classes:
            print("** class doesn't exist **")
        else:
            obj_list = []
            for obj in storage.all().values():
                if len(arg_list) > 0 and arg_list[0] == obj.__class__.__name__:
                    obj_list.append(obj.__str__())
                elif len(arg_list) == 0:
                    obj_list.append(obj.__str__())
            print(obj_list)

    def destroyInst(self, argument):
        """To delete a class instance of a given id.
        Usage: destroy <class> <id> or <class>.destroy(<id>)"""
        obj_dict = storage.all()
        arg_list = parse_arguments(argument)
        if len(arg_list) == 0:
            print("** class name missing **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        elif arg_list[0] not in HBnBCommand.available_classes:
            print("** class doesn't exist **")
        elif "{}.{}".format(arg_list[0], arg_list[1]) not in obj_dict.keys():
            print("** no instance found **")
        else:
            del obj_dict["{}.{}".format(arg_list[0], arg_list[1])]
            storage.save()

    def countInst(self, argument):
        """To retrieve the number of instances of a given class.
        Usage: count <class> or <class>.count()"""
        count = 0
        arg_list = parse_arguments(argument)
        for obj in storage.all().values():
            arg_list[0] == obj.__class__.__name__:
                count = count + 1
        print(count)

    def updateInst(self, argument):
        """To update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary.
        Usage: <class>.update(<id>, <attribute_name>, <attribute_value>)
        or update <class> <id> <attribute_name> <attribute_value>
        or <class>.update(<id>, <dictionary>)"""
        obj_dict = storage.all()
        arg_list = parse_arguments(argument)
        if arg_list[0] not in HBnBCommand.available_classes:
            print("** class doesn't exist **")
            return False
        elif "{}.{}".format(arg_list[0], arg_list[1]) not in obj_dict.keys():
            print("** no instance found **")
            return False
        elif len(arg_list) == 0:
            print("** class name missing **")
            return False
        elif len(arg_list) == 1:
            print("** instance id missing **")
            return False
        elif len(arg_list) == 2:
            print("** attribute name missing **")
            return False
        elif len(arg_list) == 3:
            try:
                type(eval(arg_list[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        elif len(arg_list) == 4:
            obj = obj_dict["{}.{}".format(arg_list[0], arg_list[1])]
            if arg_list[2] in obj.__class__.__dict__.keys():
                val_type = type(obj.__class__.__dict__[arg_list[2]])
                obj.__dict__[arg_list[2]] = val_type(arg_list[3])
            else:
                obj.__dict__[arg_list[2]] = arg_list[3]
        elif type(eval(arg_list[2])) == dict:
            obj = obj_dict["{}.{}".format(arg_list[0], arg_list[1])]
            for x, y in eval(arg_list[2]).items():
                if (x in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[x]) in {str, int, float}):
                    val_type = type(obj.__class__.__dict__[x])
                    obj.__dict__[k] = valtype(y)
                else:
                    obj.__dict__[x] = y
        storage.save()

if __name__ == "__main__":
    HBnBConsole().cmdloop()
