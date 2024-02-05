import json
import yaml
import os
import re
from datetime import datetime

def read_catalog(filename='catalog.json'):
    with open(filename, 'r') as file:
        return json.load(file)

def read_yaml_file(app_name, version, filename):
    yaml_file_path = os.path.join('home', app_name, version, filename)
    try:
        with open(yaml_file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"File {yaml_file_path} not found.")
        return {}

def get_app_versions(app_name):
    versions_path = os.path.join('home', app_name)
    try:
        version_dirs = [d for d in os.listdir(versions_path) if os.path.isdir(os.path.join(versions_path, d)) and re.match(r'^\d+\.\d+\.\d+$', d)]
        return sorted(version_dirs, key=lambda x: [int(part) for part in x.split('.')])
    except FileNotFoundError:
        print(f"Directory {versions_path} not found.")
        return []

def generate_app_versions_data(app_name, version):
    questions_data = read_yaml_file(app_name, version, 'questions.yaml')
    metadata_data = read_yaml_file(app_name, version, 'metadata.yaml')
    
    location = f"/__w/home/{app_name}/{version}"
    last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Example of generating app version data, replace and expand as necessary
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
        "chart_metadata": {
            # Placeholder values, adjust according to your needs
        }
    }
    return app_version_data

def read_existing_versions(filename='app_versions.json'):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def write_app_versions(app_versions, filename='app_versions.json'):
    with open(filename, 'w') as file:
        json.dump(app_versions, file, indent=4)

def main():
    app_name = 'idractool'  # Example app name, replace as necessary
    existing_versions = read_existing_versions()
    updated = False

    for version in get_app_versions(app_name):
        if version not in existing_versions:
            print(f"Processing version {version} for {app_name}...")
            app_version_data = generate_app_versions_data(app_name, version)
            existing_versions[version] = app_version_data
            updated = True
        else:
            print(f"Version {version} already exists for {app_name}, skipping...")

    if updated:
        write_app_versions(existing_versions)
        print(f"Updated {app_name}_versions.json with new versions.")
    else:
        print(f"No new versions to update for {app_name}.")

if __name__ == "__main__":
    main()
