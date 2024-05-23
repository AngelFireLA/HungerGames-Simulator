import random


class Tribut:
    def __init__(self, name, district=None, icon=None, gender=None, status="alive"):
        self.name = name
        self.icon = icon
        self.gender = gender
        self.status = status
        self.kills = 0
        self.inventory = []
        self.district = district

    def add_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)


class Day:
    def __init__(self, number):
        self.number = number
        self.events = []

    def add_event(self, event):
        self.events.append(event)


class Event:
    def __init__(self, description, tributes_involved):
        self.description = description
        self.tributes_involved = tributes_involved

    def execute(self):
        pass  # Define what happens during this event


class Action:
    def __init__(self, description, tributes_involved):
        self.description = description
        self.tributes_involved = tributes_involved

    def perform(self):
        pass  # Define the action's outcome

    def kill(self, killers: list, killed: list):
        # Add a kill to killers, transfer inventory randomly between killers, change status
        for dead in killed:
            dead.status = "dead"

        for killer in killers:
            killer.kills += len(killed)

        # Collect all items from the killed tributes
        all_items = []
        for dead in killed:
            all_items.extend(dead.inventory)
            dead.inventory = []  # Clear the dead tribute's inventory

        # Shuffle the collected items
        random.shuffle(all_items)

        # Distribute the items evenly among the killers
        self.distribute_items(killers, all_items)

    def distribute_items(self, killers, items):
        num_killers = len(killers)
        num_items = len(items)

        # Calculate base distribution and remainder
        base_items_per_killer = num_items // num_killers
        remainder_items = num_items % num_killers

        # Distribute base items
        item_index = 0
        for killer in killers:
            for _ in range(base_items_per_killer):
                if item_index < num_items:
                    killer.add_item(items[item_index])
                    item_index += 1

        # Distribute remainder items randomly
        random_killers = random.sample(killers, remainder_items)
        for killer in random_killers:
            if item_index < num_items:
                killer.add_item(items[item_index])
                item_index += 1


class Item:
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect

    def use(self, tribute):
        pass  # Define what happens when the item is used


class Game:
    def __init__(self):
        self.tributes = []
        self.days = []

    def add_tribute(self, tribute):
        self.tributes.append(tribute)

    def start_new_day(self):
        day_number = len(self.days) + 1
        new_day = Day(day_number)
        self.days.append(new_day)
        return new_day

    def generate_event(self, day, event):
        day.add_event(event)

    def perform_action(self, action):
        action.perform()
