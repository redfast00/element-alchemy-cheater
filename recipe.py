#!/usr/bin/env python3
from pprint import pformat
import json
import cmd

class RecipeCheater(cmd.Cmd):

    prompt = ':> '

    def __init__(self, r = None):
        assert isinstance(r, RecipeReader)
        self.r = r
        self.item_names = self.r.get_items()
        super(RecipeCheater, self).__init__()

    def completedefault(self, text, line, begidx, endidx):
        cmd = line.split(' ', 1)[0]
        if cmd in ['r', 'recipe', 'usage', 'u']:
            mline = line.partition(' ')[2]
            offs = len(mline) - len(text)
            return [s[offs:] for s in self.item_names if s.startswith(mline)]
        return []

    def default(self, line):
        parts = line.split(' ', 1)
        cmd = parts[0]
        args = ''
        if len(parts) > 1:
            args = parts[1]
        if cmd in ['r', 'recipe']:
            self.do_recipe(args)
        elif cmd in ['u', 'usage']:
            self.do_usage(args)
        elif cmd in ['d', 'dump']:
            self.do_dump(args)
        elif cmd in ['l', 'ls', 'list']:
            self.do_list(args)
        elif cmd in ['s', 'stat']:
            self.do_stat(args)
        elif cmd in ['q', 'quit', 'exit']:
            return self.do_EOF(args)
        else:
            self.stdout.write('*** Unknown syntax: %s\n'%line)

    def main(self):
        self.cmdloop()

    def do_EOF(self, line):
        """Exit"""
        self.stdout.write('\n')
        return True

    def do_recipe(self, item_name):
        """recipe [item_name]
        Prints all recipes that use specified item"""
        if not item_name:
            self.stdout.write("Please provide an item name\n")
        else:
            item_id = self.r.name_to_id(item_name)
            if not item_id:
                self.stdout.write("Item doesn't exist\n")
            else:
                recipes = self.r.lookup_recipes(item_id)
                for recipe in recipes:
                    self.stdout.write(pformat(self.r.translate_recipe(recipe)) + '\n')

    def do_usage(self, item_name):
        """usage [item_name]
        Print usage in recipes for item"""
        if not item_name:
            self.stdout.write("Please provide an item name\n")
        else:
            item_id = self.r.name_to_id(item_name)
            if not item_id:
                self.stdout.write("Item doesn't exist\n")
            else:
                recipes = self.r.lookup_uses(item_id)
                for recipe in recipes:
                    self.stdout.write(pformat(self.r.translate_recipe(recipe)) + '\n')

    def do_dump(self, filename):
        """dump [filename]
        Dumps current recipes and names in JSON format to specified file"""
        try:
            with open(filename, 'w') as dumpfile:
                dumpfile.write(self.r.dump_json())
            self.stdout.write("Succesfully saved file\n")
        except(IOError):
            self.stdout.write("Could not open file for writing\n")
            if not filename:
                self.stdout.write("Please specify filename\n")

    def do_list(self, args):
        """list
        Lists all items"""
        all_items = self.r.get_items()
        self.stdout.write(pformat(all_items))
        self.stdout.write("\nTotal: {} different items\n".format(len(all_items)))

    def do_stat(self, args):
        """stat
        Displays stats about loaded names and recipes"""
        self.stdout.write("Total: {} different items\n".format(len(self.r.names)))
        self.stdout.write("Total: {} recipes\n".format(len(self.r.recipes)))


class RecipeReader():
    """ A recipe is a dictionary like
        {"ingredients": [1, 2], "results": [8, 9]}
        itemids are always integers
        names are always lowercase
    """

    def __init__(self, recipes = None, names = None):
        """ @param recipes: a list of recipes
                ex. [{"ingredients": [1, 2], "results": [8, 9]}, {"ingredients": [1, 9], "results": [7]}]
            @param names: a dictionary that maps a name to an id
                ex. {1 : "fire", 2 : "water", 3 : "earth"}
        """
        assert names is not None
        assert recipes is not None
        self.recipes = recipes
        self.names = names

    def id_to_name(self, search_id):
        return self.names[search_id]

    def name_to_id(self, search_name):
        for itemid, name in self.names.items():
            if name == search_name:
                return itemid

    def lookup_recipes(self, search_id):
        return [recipe for recipe in self.recipes if (search_id in recipe['results'])]

    def translate_recipe(self, recipe):
        ingredients = list(map(self.id_to_name, recipe['ingredients']))
        results = list(map(self.id_to_name, recipe['results']))
        return {'ingredients': ingredients, 'results': results}

    def lookup_uses(self, search_id):
        return [recipe for recipe in self.recipes if (search_id in recipe['ingredients'])]

    def get_items(self):
        return list(self.names.values())

    def dump_json(self):
        return json.dumps({'recipes': self.recipes, 'names': self.names}, indent=2, sort_keys=True)
