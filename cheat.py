#!/usr/bin/env python3
import argparse
import json
from recipe import RecipeReader, RecipeCheater
import sys

## Parse CLI arguments
p = argparse.ArgumentParser()
p.add_argument("JSONrecipe")
args = p.parse_args()

recipe_data = {}
with open(args.JSONrecipe, 'r') as recipe_file:
    recipe_data = json.load(recipe_file)

recipes = recipe_data['recipes']

# item_id's are integers
names = {int(item_id):name for item_id, name in recipe_data['names'].items()}

reader = RecipeReader(names = names, recipes = recipes)
RecipeCheater(r = reader).main()
