#!/usr/bin/python3
"""
The Airbnb-clone Console
"""
import cmd
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.city import City
from models.state import State


class HBnBCmd(cmd.Cmd):
    """
    The entry point for the cmd interpreter
    """
    prompt = '(hbnb) '
    classes = ['BaseModel', 'User', 'Place', 'State',
               'City', 'Amenity', 'Review']
    dotcmds = ['.all()', '.count()']

    def doCreate(self, ln):
        """Creates a new instance of a given class then saves it \
(to the JSON file) and displays its id."""
        if ln not in HBnBCmd.classes:
            print('** class name doesn\'t exist **')
        elif ln == '':
            print('** class name missing **')
        else:
            if ln == 'BaseModel':
                obj = BaseModel()
            elif ln == 'User':
                obj = User()
            elif ln == 'Place':
                obj = Place()
            elif ln == 'State':
                obj = State()
            elif ln == 'City':
                obj = City()
            elif ln == 'Amenity':
                obj = Amenity()
            elif ln == 'Review':
                obj = Review()
            storage.save()
            print(obj.id)

    def doShow(self, ln):
        """Prints the string rep of an instance given \
the class name and id."""
        args = ln.split()
        if ln == '':
            print('** class name missing **')
        elif args[0] not in HBnBCmd.classes:
            print('** class name does not exist **')
        else:
            if len(args) < 2:
                print('** instance id missing **')
            else:
                classname = args[0]
                objId = args[1]
                key = classname + '.' + objId
                try:
                    print(storage.all()[key])
                except KeyError:
                    print('** no instance found **')

    def doDestroy(self, ln):
        """
        Deletes an instance given the class name
        and id then saves the change into the JSON file
        """
        args = ln.split()
        if ln == '':
            print('** class name missing **')
        elif args[0] not in HBnBCmd.classes:
            print('** class doesn\'t exist **')
        else:
            if len(args) < 2:
                print('** instance id missing **')
            else:
                classname = args[0]
                objId = args[1]
                key = classname + '.' + objId
                try:
                    del storage.all()[key]
                    storage.save()
                except KeyError:
                    print('** no instance found **')

    def doAll(self, ln):
        """
        Prints all rep of all instances in str format
        given class name. Ex: $ all BaseModel or $ all
        """
        args = ln.split()
        result = []
        if len(args) != 0:
            if args[0] not in HBnBCmd.classes:
                print('** class doesn\'t exist **')
                return
            else:
                for key, value in storage.all().items():
                    if type(value).__name__ == args[0]:
                        result.append(value.__str__())
        else:
            for key, value in storage.all().items():
                result.append(value.__str__())
        print(result)

    def doUpdate(self, ln):
        """
        Updates an instance given the class name and
        id then save the change into the JSON file  Eg: $ update
        BaseModel 1234-1234-1234 email "hbnb@gmail.com".
        update <class name> <id> <attribute name> "<attribute value>"
        """
        args = ln.split()
        if ln == '':
            print('** class name missing **')
        elif args[0] not in HBnBCmd.classes:
            print('** class doesn\'t exist **')
        elif len(args) < 2:
            print('** instance id missing **')
        elif len(args) < 3:
            print('** attribute name missing **')
        elif len(args) < 4:
            print('** value missing **')
        else:
            classname = args[0]
            objId = args[1]
            attr = args[2]
            value = args[3]
            ob = ['id', 'created_at', 'updated_at']
            if attr in ob:
                print('** attribute can\'t be updated **')
                return
            """
            check if string is valid
            """
            if value[0] == '"' and value[-1] == '"' or value[0] == "'":
                if value[0] != '"':
                    print("** A string argument must be between \
double quotes **")
                    return
                value = value[1:-1]
            else:
                try:
                    for c in value:
                        if c == '.':
                            value = float(value)
                            break
                    else:
                        value = int(value)
                except ValueError:
                    print("** A string argument must \
be between double quote **")
            if (attr[0] == '"' and attr[-1] == '"')\
               or attr[0] == "'" or attr[-1] == "'":
                if attr[0] != '"' or attr[-1] == "'":
                    print("** A string argument must be between \
double quotes **")
                    return
                attr = attr[1:-1]
            """ checking if string is valid ends here """
            key = classname + '.' + objId
            try:
                instance = storage.all()[key]
                instance.__dict__[attr] = value
                instance.save()
            except KeyError:
                print('** no instance found **')

    def doBaseModel(self, ln):
        objects = []
        parse_line = cmd.Cmd.parseline(self, ln)
        arg = parse_line[2]

        for key, value in storage.all().items():
            if type(value).__name__ == 'BaseModel':
                objects.append(value)

        if arg in HBnBCmd.dotcmds:
            result = [value.__str__() for value in objects]
            if arg == HBnBCmd.dotcmds[0]:
                print(result)
            elif arg == HBnBCmd.dotcmds[1]:
                print(len(result))

        elif arg[0:6] == '.show(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, ln)
            else:
                model_id = arg[6:-1]
                if model_id == '':
                    print("** instance id missing **")
                    return
                for obj in objects:
                    if obj.id == model_id:
                        print(obj)
                        break
                else:
                    print('** no instance found **')

        elif arg[0:9] == '.destroy(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, ln)
            else:
                model_id = arg[9:-1]
                if model_id == '':
                    print("** instance id missing **")
                    return
                key = 'BaseModel.' + model_id
                try:
                    del storage.all()[key]
                    storage.save()
                except KeyError:
                    print('** no instance found **')

        elif arg[0:8] == '.update(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, ln)
            else:
                args = arg[8:-1]
                args_list = args.split(',')
                oob = ['id', 'created_at', 'updated_at']

                if len(args_list) < 2 and args_list[0] == '':
                    print('** instance id missing **')
                    return
                elif len(args_list) < 2:
                    print('** attribute name missing **')
                    return
                else:
                    # clear whitespaces around arguments
                    i = 0
                    while (i < len(args_list)):
                        while(args_list[i][0] == " "):
                            args_list[i] = args_list[i][1:]
                        i += 1

                    if args_list[1][0] == '{' and args_list[-1][-1] == '}':
                        dict_args = args_list[1:]
                        dict_args[0] = dict_args[0][1:]
                        dict_args[-1] = dict_args[-1][:-1]
                        key = 'BaseModel.' + args_list[0]
                        try:
                            instance = storage.all()[key]
                        except KeyError:
                            print('** no instance found **')
                            return
                        for s in dict_args:
                            keyval = s.split(':')
                            key = keyval[0]
                            value = keyval[1]
                            while(value[0] == " "):
                                value = value[1:]
                            if key in oob:
                                print('** attribute can\'t be updated **')
                                return
                            if (key[0] == '"' and key[-1] == '"')\
                               or (key[0] == "'" and key[-1] == "'"):
                                key = key[1:-1]
                            else:
                                print("** Dictionary object keys must be \
strings **")
                                return
                            if (value[0] == '"' and value[-1] == '"')\
                               or (value[0] == "'" and value[-1] == "'"):
                                value = value[1:-1]

                            else:
                                for c in value:
                                    if c == " ":
                                        print("** A string argument with a \
space must be between double quotes **")
                                        return
                                try:
                                    for c in value:
                                        if c == '.':
                                            value = float(value)
                                            break
                                    else:
                                        value = int(value)
                                except ValueError:
                                    pass

                            instance.__dict__[key] = value
                            instance.save()
                        return
                    elif len(args_list) < 3:
                        print('** value missing **')
                        return

                model_id = args_list[0]
                attr = args_list[1]
                value = args_list[2]

                if attr in oob:
                    print('** attribute can\'t be updated **')
                    return
                """
                string validity test
                """
                if (attr[0] == '"' and attr[-1] == '"'):
                    attr = attr[1:-1]
                else:
                    for i in attr:
                        if i == " ":
                            print("** A string argument with a space \
must be between double quotes **")
                            return
                if value[0] == '"' and value[-1] == '"':
                    value = value[1:-1]
                else:
                    for i in attr:
                        if i == " ":
                            print("** A string argument with a space \
must be between double quotes **")
                            return
                    try:
                        for c in value:
                            if c == '.':
                                value = float(value)
                                break
                        else:
                            value = int(value)
                    except ValueError:
                        pass
                """ end of string validity test """

                key = 'BaseModel.' + model_id
                try:
                    instance = storage.all()[key]
                    instance.__dict__[attr] = value
                    instance.save()
                except KeyError:
                    print('** no instance found **')

        else:
            return cmd.Cmd.default(self, ln)

    def doUser(self, ln):
        objects = []
        parse_line = cmd.Cmd.parseline(self, ln)
        arg = parse_line[2]

        for key, value in storage.all().items():
            if type(value).__name__ == 'User':
                objects.append(value)

        if arg in HBnBCmd.dotcmds:
            result = [value.__str__() for value in objects]
            if arg == HBnBCmd.dotcmds[0]:
                print(result)
            elif arg == HBnBCmd.dotcmds[1]:
                print(len(result))

        elif arg[0:6] == '.show(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, ln)
            else:
                model_id = arg[6:-1]
                if model_id == '':
                    print("** instance id missing **")
                    return
                for obj in objects:
                    if obj.id == model_id:
                        print(obj)
                        break
                else:
                    print('** no instance found **')

        elif arg[0:9] == '.destroy(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, ln)
            else:
                model_id = arg[9:-1]
                if model_id == '':
                    print("** instance id missing **")
                    return
                key = 'User.' + model_id
                try:
                    del storage.all()[key]
                    storage.save()
                except KeyError:
                    print('** no instance found **')

        elif arg[0:8] == '.update(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, ln)
            else:
                args = arg[8:-1]
                args_list = args.split(',')
                oob = ['id', 'created_at', 'updated_at']

                if len(args_list) < 2 and args_list[0] == '':
                    print('** instance id missing **')
                    return
                elif len(args_list) < 2:
                    print('** attribute name missing **')
                    return
                else:
                    # clear whitespaces around arguments
                    i = 0
                    while (i < len(args_list)):
                        while(args_list[i][0] == " "):
                            args_list[i] = args_list[i][1:]
                        i += 1

                    if args_list[1][0] == '{' and args_list[-1][-1] == '}':
                        dict_args = args_list[1:]
                        dict_args[0] = dict_args[0][1:]
                        dict_args[-1] = dict_args[-1][:-1]
                        key = 'User.' + args_list[0]
                        try:
                            instance = storage.all()[key]
                        except KeyError:
                            print('** no instance found **')
                            return
                        for s in dict_args:
                            keyval = s.split(':')
                            key = keyval[0]
                            value = keyval[1]
                            while(value[0] == " "):
                                value = value[1:]
                            if key in oob:
                                print('** attribute can\'t be updated **')
                                return
                            if (key[0] == '"' and key[-1] == '"')\
                               or (key[0] == "'" and key[-1] == "'"):
                                key = key[1:-1]
                            else:
                                print("** Dictionary object keys must be \
strings **")
                                return
                            if (value[0] == '"' and value[-1] == '"')\
                               or (value[0] == "'" and value[-1] == "'"):
                                value = value[1:-1]

                            else:
                                for c in value:
                                    if c == " ":
                                        print("** A string argument with a \
space must be between double quotes **")
                                        return
                                try:
                                    for c in value:
                                        if c == '.':
                                            value = float(value)
                                            break
                                    else:
                                        value = int(value)
                                except ValueError:
                                    pass

                            instance.__dict__[key] = value
                            instance.save()
                        return
                    elif len(args_list) < 3:
                        print('** value missing **')
                        return

                model_id = args_list[0]
                attr = args_list[1]
                value = args_list[2]

                if attr in oob:
                    print('** attribute can\'t be updated **')
                    return
                """
                string validity test begins (incomplete)
                """
                if (attr[0] == '"' and attr[-1] == '"'):
                    attr = attr[1:-1]
                else:
                    for i in attr:
                        if i == " ":
                            print("** A string argument with a space \
must be between double quotes **")
                            return
                if value[0] == '"' and value[-1] == '"':
                    value = value[1:-1]
                else:
                    for i in attr:
                        if i == " ":
                            print("** A string argument with a space \
must be between double quotes **")
                            return
                    try:
                        for c in value:
                            if c == '.':
                                value = float(value)
                                break
                        else:
                            value = int(value)
                    except ValueError:
                        pass
                """ string validity test ends """

                key = 'User.' + model_id
                try:
                    instance = storage.all()[key]
                    instance.__dict__[attr] = value
                    instance.save()
                except KeyError:
                    print('** no instance found **')

        else:
            return cmd.Cmd.default(self, ln)

    def do_Place(self, ln):
        objects = []
        parse_line = cmd.Cmd.parseline(self, ln)
        arg = parse_line[2]

        for key, value in storage.all().items():
            if type(value).__name__ == 'Place':
                objects.append(value)

        if arg in HBnBCmd.dotcmds:
            result = [value.__str__() for value in objects]
            if arg == HBnBCmd.dotcmds[0]:
                print(result)
            elif arg == HBnBCmd.dotcmds[1]:
                print(len(result))

        elif arg[0:6] == '.show(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, ln)
            else:
                model_id = arg[6:-1]
                if model_id == '':
                    print("** instance id missing **")
                    return
                for obj in objects:
                    if obj.id == model_id:
                        print(obj)
                        break
                else:
                    print('** no instance found **')

        elif arg[0:9] == '.destroy(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, ln)
            else:
                model_id = arg[9:-1]
                if model_id == '':
                    print("** instance id missing **")
                    return
                key = 'Place.' + model_id
                try:
                    del storage.all()[key]
                    storage.save()
                except KeyError:
                    print('** no instance found **')

        elif arg[0:8] == '.update(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, ln)
            else:
                args = arg[8:-1]
                args_list = args.split(',')
                oob = ['id', 'created_at', 'updated_at']

                if len(args_list) < 2 and args_list[0] == '':
                    print('** instance id missing **')
                    return
                elif len(args_list) < 2:
                    print('** attribute name missing **')
                    return
                else:
                    # clear whitespaces around arguments
                    i = 0
                    while (i < len(args_list)):
                        while(args_list[i][0] == " "):
                            args_list[i] = args_list[i][1:]
                        i += 1

                    if args_list[1][0] == '{' and args_list[-1][-1] == '}':
                        dict_args = args_list[1:]
                        dict_args[0] = dict_args[0][1:]
                        dict_args[-1] = dict_args[-1][:-1]
                        key = 'Place.' + args_list[0]
                        try:
                            instance = storage.all()[key]
                        except KeyError:
                            print('** no instance found **')
                            return
                        for s in dict_args:
                            keyval = s.split(':')
                            key = keyval[0]
                            value = keyval[1]
                            while(value[0] == " "):
                                value = value[1:]
                            if key in oob:
                                print('** attribute can\'t be updated **')
                                return
                            if (key[0] == '"' and key[-1] == '"')\
                               or (key[0] == "'" and key[-1] == "'"):
                                key = key[1:-1]
                            else:
                                print("** Dictionary object keys must be \
strings **")
                                return
                            if (value[0] == '"' and value[-1] == '"')\
                               or (value[0] == "'" and value[-1] == "'"):
                                value = value[1:-1]

                            else:
                                for c in value:
                                    if c == " ":
                                        print("** A string argument with a \
space must be between double quotes **")
                                        return
                                try:
                                    for c in value:
                                        if c == '.':
                                            value = float(value)
                                            break
                                    else:
                                        value = int(value)
                                except ValueError:
                                    pass

                            instance.__dict__[key] = value
                            instance.save()
                        return
                    elif len(args_list) < 3:
                        print('** value missing **')
                        return

                model_id = args_list[0]
                attr = args_list[1]
                value = args_list[2]

                if attr in oob:
                    print('** attribute can\'t be updated **')
                    return
                """
                string validity test begins (incomplete)
                """
                if (attr[0] == '"' and attr[-1] == '"'):
                    attr = attr[1:-1]
                else:
                    for i in attr:
                        if i == " ":
                            print("** A string argument with a space \
must be between double quotes **")
                            return
                if value[0] == '"' and value[-1] == '"':
                    value = value[1:-1]
                else:
                    for i in attr:
                        if i == " ":
                            print("** A string argument with a space \
must be between double quotes **")
                            return
                    try:
                        for c in value:
                            if c == '.':
                                value = float(value)
                                break
                        else:
                            value = int(value)
                    except ValueError:
                        pass
                """ string validity test ends """

                key = 'Place.' + model_id
                try:
                    instance = storage.all()[key]
                    instance.__dict__[attr] = value
                    instance.save()
                except KeyError:
                    print('** no instance found **')

        else:
            return cmd.Cmd.default(self, ln)

    def doState(self, ln):
        objects = []
        parse_line = cmd.Cmd.parseline(self, ln)
        arg = parse_line[2]

        for key, value in storage.all().items():
            if type(value).__name__ == 'State':
                objects.append(value)

        if arg in HBnBCmd.dotcmds:
            result = [value.__str__() for value in objects]
            if arg == HBnBCmd.dotcmds[0]:
                print(result)
            elif arg == HBnBCmd.dotcmds[1]:
                print(len(result))

        elif arg[0:6] == '.show(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, ln)
            else:
                model_id = arg[6:-1]
                if model_id == '':
                    print("** instance id missing **")
                    return
                for obj in objects:
                    if obj.id == model_id:
                        print(obj)
                        break
                else:
                    print('** no instance found **')

        elif arg[0:9] == '.destroy(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, ln)
            else:
                model_id = arg[9:-1]
                if model_id == '':
                    print("** instance id missing **")
                    return
                key = 'State.' + model_id
                try:
                    del storage.all()[key]
                    storage.save()
                except KeyError:
                    print('** no instance found **')

        elif arg[0:8] == '.update(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, ln)
            else:
                args = arg[8:-1]
                args_list = args.split(',')
                oob = ['id', 'created_at', 'updated_at']

                if len(args_list) < 2 and args_list[0] == '':
                    print('** instance id missing **')
                    return
                elif len(args_list) < 2:
                    print('** attribute name missing **')
                    return
                else:
                    # clear whitespaces around arguments
                    i = 0
                    while (i < len(args_list)):
                        while(args_list[i][0] == " "):
                            args_list[i] = args_list[i][1:]
                        i += 1

                    if args_list[1][0] == '{' and args_list[-1][-1] == '}':
                        dict_args = args_list[1:]
                        dict_args[0] = dict_args[0][1:]
                        dict_args[-1] = dict_args[-1][:-1]
                        key = 'State.' + args_list[0]
                        try:
                            instance = storage.all()[key]
                        except KeyError:
                            print('** no instance found **')
                            return
                        for s in dict_args:
                            keyval = s.split(':')
                            key = keyval[0]
                            value = keyval[1]
                            while(value[0] == " "):
                                value = value[1:]
                            if key in oob:
                                print('** attribute can\'t be updated **')
                                return
                            if (key[0] == '"' and key[-1] == '"')\
                               or (key[0] == "'" and key[-1] == "'"):
                                key = key[1:-1]
                            else:
                                print("** Dictionary object keys must be \
strings **")
                                return
                            if (value[0] == '"' and value[-1] == '"')\
                               or (value[0] == "'" and value[-1] == "'"):
                                value = value[1:-1]

                            else:
                                for c in value:
                                    if c == " ":
                                        print("** A string argument with a \
space must be between double quotes **")
                                        return
                                try:
                                    for c in value:
                                        if c == '.':
                                            value = float(value)
                                            break
                                    else:
                                        value = int(value)
                                except ValueError:
                                    pass

                            instance.__dict__[key] = value
                            instance.save()
                        return
                    elif len(args_list) < 3:
                        print('** value missing **')
                        return

                model_id = args_list[0]
                attr = args_list[1]
                value = args_list[2]

                if attr in oob:
                    print('** attribute can\'t be updated **')
                    return
                """
                string validity test begins (incomplete)
                """
                if (attr[0] == '"' and attr[-1] == '"'):
                    attr = attr[1:-1]
                else:
                    for i in attr:
                        if i == " ":
                            print("** A string argument with a space \
must be between double quotes **")
                            return
                if value[0] == '"' and value[-1] == '"':
                    value = value[1:-1]
                else:
                    for i in attr:
                        if i == " ":
                            print("** A string argument with a space \
must be between double quotes **")
                            return
                    try:
                        for c in value:
                            if c == '.':
                                value = float(value)
                                break
                        else:
                            value = int(value)
                    except ValueError:
                        pass
                """ string validity test ends """

                key = 'State.' + model_id
                try:
                    instance = storage.all()[key]
                    instance.__dict__[attr] = value
                    instance.save()
                except KeyError:
                    print('** no instance found **')

        else:
            return cmd.Cmd.default(self, ln)

    def doCity(self, ln):
        objects = []
        parse_line = cmd.Cmd.parseline(self, ln)
        arg = parse_line[2]

        for key, value in storage.all().items():
            if type(value).__name__ == 'City':
                objects.append(value)

        if arg in HBnBCmd.dotcmds:
            result = [value.__str__() for value in objects]
            if arg == HBnBCmd.dotcmds[0]:
                print(result)
            elif arg == HBnBCmd.dotcmds[1]:
                print(len(result))

        elif arg[0:6] == '.show(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, ln)
            else:
                model_id = arg[6:-1]
                if model_id == '':
                    print("** instance id missing **")
                    return
                for obj in objects:
                    if obj.id == model_id:
                        print(obj)
                        break
                else:
                    print('** no instance found **')

        elif arg[0:9] == '.destroy(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, ln)
            else:
                model_id = arg[9:-1]
                if model_id == '':
                    print("** instance id missing **")
                    return
                key = 'City.' + model_id
                try:
                    del storage.all()[key]
                    storage.save()
                except KeyError:
                    print('** no instance found **')

        elif arg[0:8] == '.update(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, ln)
            else:
                args = arg[8:-1]
                args_list = args.split(',')
                oob = ['id', 'created_at', 'updated_at']

                if len(args_list) < 2 and args_list[0] == '':
                    print('** instance id missing **')
                    return
                elif len(args_list) < 2:
                    print('** attribute name missing **')
                    return
                else:
                    # clear whitespaces around arguments
                    i = 0
                    while (i < len(args_list)):
                        while(args_list[i][0] == " "):
                            args_list[i] = args_list[i][1:]
                        i += 1

                    if args_list[1][0] == '{' and args_list[-1][-1] == '}':
                        dict_args = args_list[1:]
                        dict_args[0] = dict_args[0][1:]
                        dict_args[-1] = dict_args[-1][:-1]
                        key = 'City.' + args_list[0]
                        try:
                            instance = storage.all()[key]
                        except KeyError:
                            print('** no instance found **')
                            return
                        for s in dict_args:
                            keyval = s.split(':')
                            key = keyval[0]
                            value = keyval[1]
                            while(value[0] == " "):
                                value = value[1:]
                            if key in oob:
                                print('** attribute can\'t be updated **')
                                return
                            if (key[0] == '"' and key[-1] == '"')\
                               or (key[0] == "'" and key[-1] == "'"):
                                key = key[1:-1]
                            else:
                                print("** Dictionary object keys must be \
strings **")
                                return
                            if (value[0] == '"' and value[-1] == '"')\
                               or (value[0] == "'" and value[-1] == "'"):
                                value = value[1:-1]

                            else:
                                for c in value:
                                    if c == " ":
                                        print("** A string argument with a \
space must be between double quotes **")
                                        return
                                try:
                                    for c in value:
                                        if c == '.':
                                            value = float(value)
                                            break
                                    else:
                                        value = int(value)
                                except ValueError:
                                    pass

                            instance.__dict__[key] = value
                            instance.save()
                        return
                    elif len(args_list) < 3:
                        print('** value missing **')
                        return

                model_id = args_list[0]
                attr = args_list[1]
                value = args_list[2]

                if attr in oob:
                    print('** attribute can\'t be updated **')
                    return
                """
                string validity test begins (incomplete)
                """
                if (attr[0] == '"' and attr[-1] == '"'):
                    attr = attr[1:-1]
                else:
                    for i in attr:
                        if i == " ":
                            print("** A string argument with a space \
must be between double quotes **")
                            return
                if value[0] == '"' and value[-1] == '"':
                    value = value[1:-1]
                else:
                    for i in attr:
                        if i == " ":
                            print("** A string argument with a space \
must be between double quotes **")
                            return
                    try:
                        for c in value:
                            if c == '.':
                                value = float(value)
                                break
                        else:
                            value = int(value)
                    except ValueError:
                        pass
                """ string validity test ends """

                key = 'City.' + model_id
                try:
                    instance = storage.all()[key]
                    instance.__dict__[attr] = value
                    instance.save()
                except KeyError:
                    print('** no instance found **')

        else:
            return cmd.Cmd.default(self, ln)

    def doAmenity(self, ln):
        objects = []
        parse_line = cmd.Cmd.parseline(self, ln)
        arg = parse_line[2]

        for key, value in storage.all().items():
            if type(value).__name__ == 'Amenity':
                objects.append(value)

        if arg in HBnBCmd.dotcmds:
            result = [value.__str__() for value in objects]
            if arg == HBnBCmd.dotcmds[0]:
                print(result)
            elif arg == HBnBCmd.dotcmds[1]:
                print(len(result))

        elif arg[0:6] == '.show(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, ln)
            else:
                model_id = arg[6:-1]
                if model_id == '':
                    print("** instance id missing **")
                    return
                for obj in objects:
                    if obj.id == model_id:
                        print(obj)
                        break
                else:
                    print('** no instance found **')

        elif arg[0:9] == '.destroy(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, ln)
            else:
                model_id = arg[9:-1]
                if model_id == '':
                    print("** instance id missing **")
                    return
                key = 'Amenity.' + model_id
                try:
                    del storage.all()[key]
                    storage.save()
                except KeyError:
                    print('** no instance found **')

        elif arg[0:8] == '.update(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, ln)
            else:
                args = arg[8:-1]
                args_list = args.split(',')
                oob = ['id', 'created_at', 'updated_at']

                if len(args_list) < 2 and args_list[0] == '':
                    print('** instance id missing **')
                    return
                elif len(args_list) < 2:
                    print('** attribute name missing **')
                    return
                else:
                    # clear whitespaces around arguments
                    i = 0
                    while (i < len(args_list)):
                        while(args_list[i][0] == " "):
                            args_list[i] = args_list[i][1:]
                        i += 1

                    if args_list[1][0] == '{' and args_list[-1][-1] == '}':
                        dict_args = args_list[1:]
                        dict_args[0] = dict_args[0][1:]
                        dict_args[-1] = dict_args[-1][:-1]
                        key = 'Amenity.' + args_list[0]
                        try:
                            instance = storage.all()[key]
                        except KeyError:
                            print('** no instance found **')
                            return
                        for s in dict_args:
                            keyval = s.split(':')
                            key = keyval[0]
                            value = keyval[1]
                            while(value[0] == " "):
                                value = value[1:]
                            if key in oob:
                                print('** attribute can\'t be updated **')
                                return
                            if (key[0] == '"' and key[-1] == '"')\
                               or (key[0] == "'" and key[-1] == "'"):
                                key = key[1:-1]
                            else:
                                print("** Dictionary object keys must be \
strings **")
                                return
                            if (value[0] == '"' and value[-1] == '"')\
                               or (value[0] == "'" and value[-1] == "'"):
                                value = value[1:-1]

                            else:
                                for c in value:
                                    if c == " ":
                                        print("** A string argument with a \
space must be between double quotes **")
                                        return
                                try:
                                    for c in value:
                                        if c == '.':
                                            value = float(value)
                                            break
                                    else:
                                        value = int(value)
                                except ValueError:
                                    pass

                            instance.__dict__[key] = value
                            instance.save()
                        return
                    elif len(args_list) < 3:
                        print('** value missing **')
                        return

                model_id = args_list[0]
                attr = args_list[1]
                value = args_list[2]

                if attr in oob:
                    print('** attribute can\'t be updated **')
                    return
                """
                string validity test begins (incomplete)
                """
                if (attr[0] == '"' and attr[-1] == '"'):
                    attr = attr[1:-1]
                else:
                    for i in attr:
                        if i == " ":
                            print("** A string argument with a space \
must be between double quotes **")
                            return
                if value[0] == '"' and value[-1] == '"':
                    value = value[1:-1]
                else:
                    for i in attr:
                        if i == " ":
                            print("** A string argument with a space \
must be between double quotes **")
                            return
                    try:
                        for c in value:
                            if c == '.':
                                value = float(value)
                                break
                        else:
                            value = int(value)
                    except ValueError:
                        pass
                """ string validity test ends """

                key = 'Amenity.' + model_id
                try:
                    instance = storage.all()[key]
                    instance.__dict__[attr] = value
                    instance.save()
                except KeyError:
                    print('** no instance found **')

        else:
            return cmd.Cmd.default(self, ln)

    def doReview(self, ln):
        objects = []
        parse_line = cmd.Cmd.parseline(self, ln)
        arg = parse_line[2]

        for key, value in storage.all().items():
            if type(value).__name__ == 'Review':
                objects.append(value)

        if arg in HBnBCmd.dotcmds:
            result = [value.__str__() for value in objects]
            if arg == HBnBCmd.dotcmds[0]:
                print(result)
            elif arg == HBnBCmd.dotcmds[1]:
                print(len(result))

        elif arg[0:6] == '.show(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, ln)
            else:
                model_id = arg[6:-1]
                if model_id == '':
                    print("** instance id missing **")
                    return
                for obj in objects:
                    if obj.id == model_id:
                        print(obj)
                        break
                else:
                    print('** no instance found **')

        elif arg[0:9] == '.destroy(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, ln)
            else:
                model_id = arg[9:-1]
                if model_id == '':
                    print("** instance id missing **")
                    return
                key = 'Review.' + model_id
                try:
                    del storage.all()[key]
                    storage.save()
                except KeyError:
                    print('** no instance found **')

        elif arg[0:8] == '.update(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, ln)
            else:
                args = arg[8:-1]
                args_list = args.split(',')
                oob = ['id', 'created_at', 'updated_at']

                if len(args_list) < 2 and args_list[0] == '':
                    print('** instance id missing **')
                    return
                elif len(args_list) < 2:
                    print('** attribute name missing **')
                    return
                else:
                    # clear whitespaces around arguments
                    i = 0
                    while (i < len(args_list)):
                        while(args_list[i][0] == " "):
                            args_list[i] = args_list[i][1:]
                        i += 1

                    if args_list[1][0] == '{' and args_list[-1][-1] == '}':
                        dictargs = args_list[1:]
                        dictargs[0] = dictargs[0][1:]
                        dictargs[-1] = dictargs[-1][:-1]
                        key = 'Review.' + args_list[0]
                        try:
                            instance = storage.all()[key]
                        except KeyError:
                            print('** no instance found **')
                            return
                        for s in dictargs:
                            keyval = s.split(':')
                            key = keyval[0]
                            value = keyval[1]
                            while(value[0] == " "):
                                value = value[1:]
                            if key in oob:
                                print('** attribute can\'t be updated **')
                                return
                            if (key[0] == '"' and key[-1] == '"')\
                               or (key[0] == "'" and key[-1] == "'"):
                                key = key[1:-1]
                            else:
                                print("** Dictionary object keys must be \
strings **")
                                return
                            if (value[0] == '"' and value[-1] == '"')\
                               or (value[0] == "'" and value[-1] == "'"):
                                value = value[1:-1]

                            else:
                                for c in value:
                                    if c == " ":
                                        print("** A string argument with a \
space must be between double quotes **")
                                        return
                                try:
                                    for c in value:
                                        if c == '.':
                                            value = float(value)
                                            break
                                    else:
                                        value = int(value)
                                except ValueError:
                                    pass

                            instance.__dict__[key] = value
                            instance.save()
                        return
                    elif len(args_list) < 3:
                        print('** value missing **')
                        return

                model_id = args_list[0]
                attr = args_list[1]
                value = args_list[2]

                if attr in oob:
                    print('** attribute can\'t be updated **')
                    return
                """
                string validity test begins (incomplete)
                """
                if (attr[0] == '"' and attr[-1] == '"'):
                    attr = attr[1:-1]
                else:
                    for i in attr:
                        if i == " ":
                            print("** A string argument with a space \
must be between double quotes **")
                            return
                if value[0] == '"' and value[-1] == '"':
                    value = value[1:-1]
                else:
                    for i in attr:
                        if i == " ":
                            print("** A string argument with a space \
must be between double quotes **")
                            return
                    try:
                        for c in value:
                            if c == '.':
                                value = float(value)
                                break
                        else:
                            value = int(value)
                    except ValueError:
                        pass
                """ string validity test ends """

                key = 'Review.' + model_id
                try:
                    instance = storage.all()[key]
                    instance.__dict__[attr] = value
                    instance.save()
                except KeyError:
                    print('** no instance found **')

        else:
            return cmd.Cmd.default(self, line)

    def doQuit(self, ln):
        """Quit command to exit from cmd"""
        return True

    def doEOF(self, ln):
        """Ctrl D - to kill the program or exit from cmd"""
        print()
        return True

    def emptyline(self):
        """Empty line + Enter shouldn't execute anything"""
        pass


if __name__ == '__main__':
    HBnBCmd().cmdloop()
