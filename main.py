import os


class Tribute:
    def __init__(self, name, gender, district, icon=None):
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
        self.is_alive = True

    def add_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)

    def change_health(self, amount):
        self.health += amount
        self.health = max(0, min(self.health, 100))  # Health should be between 0 and 100
        if amount > 0:
            print(f"{self.name} +{amount}❤️ ({self.health}❤️)")
        else:
            print(f"{self.name} {amount}❤️ ({self.health}❤️)")
        if self.health == 0:
            self.is_alive = False
            print(f"{self.name} 💀")

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
        return (
            f"Tribute(name={self.name}, gender={self.gender}, district={self.district}, "
            f"health={self.health}, hunger={self.hunger}, thirst={self.thirst}, "
            f"combat_power={self.combat_power}, stealth={self.stealth}, vision={self.vision}, "
            f"charisma={self.charisma}, inventory={self.inventory}, kill_count={self.kill_count}, "
            f"is_alive={self.is_alive})"
        )


class Action:
    def __init__(self, name, description, usually_lethal, num_affected, num_killers, killers, stats_changes,
                 bonus_items=None, removed_items=None, relation_changes=None, requirements=None):
        self.name = name
        self.description = description
        self.usually_lethal = usually_lethal
        self.num_affected = num_affected
        self.num_killers = num_killers
        self.killers = killers
        self.stats_changes = stats_changes or {}
        self.bonus_items = bonus_items or {}
        self.removed_items = removed_items or {}
        self.relation_changes = relation_changes or {}
        self.requirements = requirements or {}

    def __repr__(self):
        return f"Action(name={self.name})"


import json
import random


class Game:
    def __init__(self, tributes, action_pools):
        self.tributes = tributes
        self.day_count = 0
        self.rankings = []
        self.action_pools = action_pools

    def run_day(self):
        input()
        self.day_count += 1
        self.run_actions(self.action_pools['day'])
        print()

    def run_night(self):
        input()
        self.run_actions(self.action_pools['night'])
        print()

    def run_actions(self, action_pool):
        available_tributes = [t for t in self.tributes if t.is_alive]
        used_tributes = set()

        while available_tributes:
            action = random.choice(action_pool)
            if len(available_tributes) < action.num_affected:
                continue  # Skip if not enough tributes are available

            selected_tributes = random.sample(available_tributes, action.num_affected)
            if self.check_requirements(selected_tributes, action.requirements):
                for tribute in selected_tributes:
                    used_tributes.add(tribute)
                self.execute_action(selected_tributes, action)

            # Update available tributes
            available_tributes = [t for t in self.tributes if t.is_alive and t not in used_tributes]

    def check_requirements(self, tributes, requirements):
        for i, tribute in enumerate(tributes):
            if str(i) in requirements:
                reqs = requirements[str(i)]
                try:
                # Check stats requirements
                    for stat, value in reqs.get('stats', {}).items():
                        if isinstance(value, dict):
                            if 'min' in value and getattr(tribute, stat) < value['min']:
                                return False
                            if 'max' in value and getattr(tribute, stat) > value['max']:
                                return False
                        elif getattr(tribute, stat) < value:
                            return False
                except AttributeError as e:
                    print(reqs)
                    raise e
                # Check items requirements
                for item in reqs.get('items', []):
                    if item.lower() not in [inv_item.lower() for inv_item in tribute.inventory]:
                        return False
                for target_index, status in reqs.get('relations', {}).items():
                    try:
                        target_name = tributes[int(target_index)].name
                    except (IndexError, ValueError):
                        return False
                    if target_name not in tribute.relations or tribute.relations[target_name] != status:
                        return False

        return True

    def execute_action(self, tributes, action):
        killed_tributes = []
        killers = []
        description = action.description
        for i, tribute in enumerate(tributes):
            description = description.replace(f"Tribute {i + 1}", tribute.name)

        print(description)
        for i, tribute in enumerate(tributes):
            if tribute.is_alive:
                # Update tribute stats based on the action
                self.apply_stats_changes(tribute, action.stats_changes.get(str(i), {}))

                # Handle item addition/removal
                for item in action.bonus_items.get(str(i), []):
                    tribute.add_item(item)
                for item in action.removed_items.get(str(i), []):
                    tribute.remove_item(item)

                # Handle relation changes
                if str(i) in action.relation_changes:
                    relation_change = action.relation_changes[str(i)]
                    target_index = relation_change['target']
                    status = relation_change['status']
                    if 0 <= target_index < len(tributes):
                        other_tribute = tributes[target_index]
                        tribute.change_relation(other_tribute, status)

                # Track killers
                if str(i) in action.killers:
                    killers.append(tribute)

                # Track killed tributes
                if action.usually_lethal and tribute.health <= 0:
                    tribute.is_alive = False
                    killed_tributes.append(tribute)

        # Distribute items from killed tributes to killers
        self.distribute_items(killed_tributes, killers)

    def distribute_items(self, killed_tributes, killers):
        if not killers:
            return

        all_items = []
        for killed in killed_tributes:
            all_items.extend(killed.inventory)
            killed.inventory.clear()

        random.shuffle(all_items)
        num_killers = len(killers)
        base_share = len(all_items) // num_killers
        extra_items = len(all_items) % num_killers

        for killer in killers:
            for _ in range(base_share):
                killer.add_item(all_items.pop(0))

        for _ in range(extra_items):
            random_killer = random.choice(killers)
            random_killer.add_item(all_items.pop(0))

    def apply_stats_changes(self, tribute, stats_change):
        if stats_change:
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
        lang_file_path = os.path.join('language_files', f'{config.language}.json')

        with open(file_path, 'r', encoding="utf-8") as file:
            data = json.load(file)

        with open(lang_file_path, 'r', encoding="utf-8") as lang_file:
            lang_data = json.load(lang_file)

        actions = []
        pool_name = os.path.splitext(os.path.basename(file_path))[0]
        for action_data in data:
            name = action_data['name']
            description_key = f"{name}_{pool_name}"
            description = Game.get_description_from_lang(lang_data, description_key)
            usually_lethal = action_data['usually_lethal']
            num_affected = action_data['num_affected']
            num_killers = action_data['num_killers']
            killers = action_data['killers']
            stats_changes = action_data['stats_changes']
            bonus_items = action_data.get('bonus_items', {})
            removed_items = action_data.get('removed_items', {})
            relation_changes = action_data.get('relation_changes', {})
            requirements = action_data.get('requirements', {})
            actions.append(
                Action(name, description, usually_lethal, num_affected, num_killers, killers, stats_changes,
                       bonus_items,
                       removed_items, relation_changes, requirements))
        return actions

    @staticmethod
    def get_description_from_lang(lang_data, description_key):
        for descriptions in lang_data.values():
            if description_key in descriptions:
                return descriptions[description_key]
        return "Description not found"

    def remaining_tributes(self):
        return [tribute for tribute in self.tributes if tribute.is_alive]

    def __repr__(self):
        return f"Game(day_count={self.day_count}, tributes_remaining={len(self.tributes)})"


class Config:
    def __init__(self, config_file):
        with open(config_file, 'r', encoding="utf-8") as file:
            config = json.load(file)
            self.language = config.get('language', 'en')

config = Config('config.json')

# Create tributes
tributes = [
]

# Load actions from JSON files
day_actions = Game.load_actions_from_json('action_pools/day.json')
night_actions = Game.load_actions_from_json('action_pools/night.json')
# the_feast_actions = Game.load_actions_from_json('the_feast.json')

# Action pools
action_pools = {
    "day": day_actions,
    "night": night_actions,
    # "the_feast": the_feast_actions
}

# Create the game
game = Game(tributes, action_pools)
print("Bienvenue aux Hunger Games, appuyez pour continuer")
while len(game.remaining_tributes()) > 1:
    game.run_day()
    game.run_night()

print(game.remaining_tributes())

