import json
import yaml
import os
import re
from datetime import datetime

# Flag to control recreation of app_versions.json files
RECREATE_ALL = False

def list_all_apps(base_path='home'):
    try:
        return [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    except FileNotFoundError:
        print(f"Base directory {base_path} not found.")
        return []

def read_yaml_file(app_path, version, filename):
    yaml_file_path = os.path.join(app_path, version, filename)
    try:
        with open(yaml_file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"File {yaml_file_path} not found.")
        return {}

def get_app_versions(app_path):
    try:
        version_dirs = [d for d in os.listdir(app_path) if os.path.isdir(os.path.join(app_path, d)) and re.match(r'^\d+\.\d+\.\d+$', d)]
        return sorted(version_dirs, key=lambda x: [int(part) for part in x.split('.')])
    except FileNotFoundError:
        print(f"App directory {app_path} not found.")
        return []

def generate_app_versions_data(app_path, version):
    questions_data = read_yaml_file(app_path, version, 'questions.yaml') or {}
    metadata_data = read_yaml_file(app_path, version, 'metadata.yaml') or {}

    metadata_data["runAsContext"] = [{
        "gid": 568,
        "uid": 568,
        "description": "Static GID and UID for runAsContext"
    }] if "runAsContext" in metadata_data else []

    location = f"/__w/{app_path}/{version}"
    last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    app_version_data = {
        "healthy": True,
        "supported": True,
        "healthy_error": None,
        "last_update": last_update,
        "required_features": ["normalize/acl", "normalize/ixVolume"],
        "human_version": version,
        "version": version,
        "location": location,
        "app_readme": questions_data.get('app_readme', ''),
        "detailed_readme": questions_data.get('detailed_readme', ''),
        "schema": {
            "groups": questions_data.get('groups', []),
            "portals": {},
            "questions": questions_data.get('questions', [])
        },
        "app_metadata": metadata_data,
    }
    return app_version_data

def write_app_versions(app_versions, app_path):
    filename = os.path.join(app_path, 'app_versions.json')
    with open(filename, 'w') as file:
        json.dump(app_versions, file, indent=4)

def process_app_versions(app_name, base_path='home'):
    app_path = os.path.join(base_path, app_name)
    if RECREATE_ALL or not os.path.exists(os.path.join(app_path, 'app_versions.json')):
        existing_versions = {}
    else:
        existing_versions = read_existing_versions(app_path)
    
    updated = False

    for version in get_app_versions(app_path):
        if RECREATE_ALL or version not in existing_versions:
            print(f"Processing version {version} for {app_name}...")
            app_version_data = generate_app_versions_data(app_path, version)
            existing_versions[version] = app_version_data
            updated = True

    if updated:
        write_app_versions(existing_versions, app_path)
        print(f"Updated versions for {app_name}.")

def read_existing_versions(app_path):
    filename = os.path.join(app_path, 'app_versions.json')
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def main():
    base_path = 'home'
    all_apps = list_all_apps(base_path)
    
    for app_name in all_apps:
        print(f"Processing {app_name}...")
        process_app_versions(app_name, base_path)

if __name__ == "__main__":
    main()
