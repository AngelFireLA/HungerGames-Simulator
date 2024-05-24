import random


class Tribute:
    def __init__(self, name, gender, district, icon):
        self.name = name
        self.gender = gender
        self.district = district
        self.icon = icon
        self.inventory = []
        self.health = 100
        self.hunger = 100
        self.thirst = 100
        self.combat_power = 50
        self.stealth = 50
        self.vision = 50
        self.charisma = 50
        self.relations = {}
        self.kill_count = 0
        self.alive = True

    def add_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)

    def change_health(self, amount):
        self.health += amount
        self.health = max(0, min(self.health, 100))  # Health should be between 0 and 100
        if self.health == 0:
            
    def change_hunger(self, amount):
        self.hunger += amount
        self.hunger = max(0, min(self.hunger, 100))  # Hunger should be between 0 and 100

    def change_thirst(self, amount):
        self.thirst += amount
        self.thirst = max(0, min(self.thirst, 100))  # Thirst should be between 0 and 100

    def change_combat_power(self, amount):
        self.combat_power += amount

    def change_stealth(self, amount):
        self.stealth += amount

    def change_vision(self, amount):
        self.vision += amount

    def change_charisma(self, amount):
        self.charisma += amount

    def change_relation(self, other_tribute, status):
        self.relations[other_tribute.name] = status

    def __repr__(self):
        return f"Tribute(name={self.name}, district={self.district}, health={self.health})"



class Day:
    def __init__(self, number):
        self.number = number
        self.events = []

    def add_event(self, event):
        self.events.append(event)



class Action:
    def __init__(self, name, description, lethal, num_affected, num_killers, num_killed, stats_changes, bonus_items=None, removed_items=None, relation_changes=None):
        self.name = name
        self.description = description
        self.lethal = lethal
        self.num_affected = num_affected
        self.num_killers = num_killers
        self.num_killed = num_killed
        self.stats_changes = stats_changes  # List of dicts for each affected tribute
        self.bonus_items = bonus_items or []  # List of items for each affected tribute
        self.removed_items = removed_items or []  # List of items for each affected tribute
        self.relation_changes = relation_changes or []  # List of dicts for each affected tribute

    def __repr__(self):
        return f"Action(name={self.name}, lethal={self.lethal})"



class Item:
    def __init__(self, name, item_type, stackable, lethal, stats_change):
        self.name = name
        self.item_type = item_type
        self.stackable = stackable
        self.lethal = lethal
        self.stats_change = stats_change

    def __repr__(self):
        return f"Item(name={self.name}, type={self.item_type})"



import json
import random

class Game:
    def __init__(self, tributes, action_pools):
        self.tributes = tributes
        self.day_count = 0
        self.rankings = []
        self.action_pools = action_pools

    def run_day(self):
        self.day_count += 1
        actions = random.sample(self.action_pools['day'], len(self.tributes))
        for tribute, action in zip(self.tributes, actions):
            self.execute_action(tribute, action)

    def run_night(self):
        actions = random.sample(self.action_pools['night'], len(self.tributes))
        for tribute, action in zip(self.tributes, actions):
            self.execute_action(tribute, action)

    def execute_action(self, tribute, action):
        if tribute.is_alive:
            # Update tribute stats based on the action
            for i, stats_change in enumerate(action.stats_changes):
                self.apply_stats_changes(tribute, stats_change)

            # Handle item addition/removal
            for i, bonus_items in enumerate(action.bonus_items):
                for item in bonus_items:
                    tribute.add_item(item)
            for i, removed_items in enumerate(action.removed_items):
                for item in removed_items:
                    tribute.remove_item(item)

            # Handle relation changes
            for relation_change in action.relation_changes:
                target_index = relation_change['target']
                status = relation_change['status']
                if 0 <= target_index < len(self.tributes):
                    other_tribute = self.tributes[target_index]
                    tribute.change_relation(other_tribute, status)

            # Handle lethal actions
            if action.lethal and tribute.health <= 0:
                tribute.is_alive = False
                self.rankings.append(tribute)
                self.tributes.remove(tribute)

    def apply_stats_changes(self, tribute, stats_change):
        for stat, change in stats_change.items():
            if stat == 'health':
                tribute.change_health(change)
            elif stat == 'hunger':
                tribute.change_hunger(change)
            elif stat == 'thirst':
                tribute.change_thirst(change)
            elif stat == 'combat_power':
                tribute.change_combat_power(change)
            elif stat == 'stealth':
                tribute.change_stealth(change)
            elif stat == 'vision':
                tribute.change_vision(change)
            elif stat == 'charisma':
                tribute.change_charisma(change)

    @staticmethod
    def load_actions_from_json(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            actions = []
            for action_data in data:
                name = action_data['name']
                description = action_data['description']
                lethal = action_data['lethal']
                num_affected = action_data['num_affected']
                num_killers = action_data['num_killers']
                num_killed = action_data['num_killed']
                stats_changes = action_data['stats_changes']
                bonus_items = action_data.get('bonus_items', [[] for _ in range(num_affected)])
                removed_items = action_data.get('removed_items', [[] for _ in range(num_affected)])
                relation_changes = action_data.get('relation_changes', [])
                actions.append(Action(name, description, lethal, num_affected, num_killers, num_killed, stats_changes, bonus_items, removed_items, relation_changes))
            return actions

    def __repr__(self):
        return f"Game(day_count={self.day_count}, tributes_remaining={len(self.tributes)})"

# Create tributes
tributes = [
    Tribute("Tribute1", "M", "District1", "icon1.png"),
    Tribute("Tribute2", "F", "District2", "icon2.png"),
    # Add more tributes
]

# Load actions from JSON files
day_actions = Game.load_actions_from_json('day.json')
night_actions = Game.load_actions_from_json('night.json')
the_feast_actions = Game.load_actions_from_json('the_feast.json')

# Action pools
action_pools = {
    "day": day_actions,
    "night": night_actions,
    "the_feast": the_feast_actions
}

# Create the game
game = Game(tributes, action_pools)

# Run the game
game.run_day()
game.run_night()

print(game)

