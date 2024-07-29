import json
import os


def create_language_files_and_update_pools(action_pool_files, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    language_data = {}

    for pool_file in action_pool_files:
        with open("action_pools/"+pool_file, 'r') as file:
            actions = json.load(file)

        for action in actions:
            name = action['name']
            description = action.pop('description')  # Remove description and get its value

            if name not in language_data:
                language_data[name] = {}
            language_data[name][pool_file] = description

            # Update action to use language key
            action['description_key'] = f"{name}_{os.path.splitext(os.path.basename(pool_file))[0]}"

        # Save the modified action pool file
        with open(pool_file, 'w') as file:
            json.dump(actions, file, indent=4)

    # Save the language files
    for lang in ['en']:
        lang_data = {}
        for name, descriptions in language_data.items():
            lang_data[name] = {}
            for pool_file, description in descriptions.items():
                key = f"{name}_{os.path.splitext(os.path.basename(pool_file))[0]}"
                lang_data[name][key] = description if lang == 'en' else f"TRANSLATION NEEDED: {description}"

        with open(os.path.join(output_dir, f'{lang}.json'), 'w') as file:
            json.dump(lang_data, file, indent=4)


# List of action pool files to process
action_pool_files = ['day.json', 'night.json']  # Add other action pool files here

# Directory to save language files
output_dir = '../language_files'

create_language_files_and_update_pools(action_pool_files, output_dir)
