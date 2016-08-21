# element-alchemy-cheater
This repository contains the recipes for some element alchemy games. It also has
a CLI to facilitate looking up recipes and usages of an item.

## What is an element alchemy game?

An element alchemy game (later EAG) is a game where you start of with the four
natural elements (air, fire, water and earth) and combine them in order to form
other elements. For example: earth + fire = lava. [Example of an EAG](https://littlealchemy.com/)

## How do I select what game I want to use?

First, determine what the reverse domain of the app is (Example: `com.sometimeswefly.littlealchemy`) and check
if it is available by checking if it is in the JSONrecipes directory. If so, run

```bash
./cheat.py JSONrecipes/<reverse domain>.json
```
(Example: `./cheat.py JSONrecipes/com.sometimeswefly.littlealchemy.json`)

If there is no recipe file for your game yet, please submit an issue or PR.

## How do I interact with the CLI? What are the available commands?

Type `help` to see a list of available commands.

## I hate typing!

Uh, okay... Tab-completion for names is available, and most commands are
aliased to their first letter.

## How did you obtain the JSON recipe files?

Read my [blog post]() (TL;DR: I reverse engineered the apps and extracted the recipes from the decompiled sources)

## How are recipe files structured?

`item_id`s are always positive integers, `names` are always lowercase strings.
A `recipe` is a dictionary with two keys: `ingredients` and `results`.
Those keys contain a list of `item_id`s. The order of the `item_id`s doesn't matter.

The JSON file has two keys: `recipes` (a list of `recipe`s) and `names` (a dictionary that maps `names` to `item_id`s)
