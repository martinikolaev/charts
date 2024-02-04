import json
import yaml  # Ensure PyYAML is installed (pip install pyyaml)
from datetime import datetime
import os

def read_catalogue(filename='catalog.json'):
    """Reads the catalogue file and returns its content as a dictionary."""
    with open(filename, 'r') as file:
        return json.load(file)

def read_yaml_file(app_name, version, filename):
    """
    Reads a YAML file (either questions.yaml or metadata.yaml) for the given app version
    and returns its content as a dictionary.
    """
    yaml_file_path = os.path.join('home', app_name, version, filename)
    try:
        with open(yaml_file_path, 'r') as file:
            yaml_data = yaml.safe_load(file)
        return yaml_data
    except FileNotFoundError:
        print(f"File {yaml_file_path} not found.")
        return {}

def generate_app_versions_data(app_data, questions_data, metadata_data):
    """
    Takes the application data extracted from the catalogue, the questions data, and the metadata data,
    and generates the structure for app_versions.json with dynamic and static values.
    """
    latest_version = app_data['latest_version']
    app_versions_data = {
        latest_version: {
            "healthy": True,
            "supported": True,
            "healthy_error": None,
            "last_update": "2024-02-03 10:49:45",
            "required_features": ["normalize/acl", "normalize/ixVolume"],
            "human_version": latest_version,
            "version": latest_version,
            "app_readme": app_data.get('app_readme', ''),
            "detailed_readme": app_data.get('app_readme', ''),
            "schema": {
                "groups": questions_data.get('groups', []),
                "portals": {},
                "questions": questions_data.get('questions', [])
            },
            "app_metadata": metadata_data,
            # Add other dynamic fields from app_data if needed
        }
    }
    return app_versions_data

def write_app_versions(app_versions_data, filename='app_versions.json'):
    """Writes the app versions data to a file."""
    with open(filename, 'w') as file:
        json.dump(app_versions_data, file, indent=4)

def main():
    catalogue = read_catalogue()  # Reads the catalogue.json file
    app_name = 'idractool'  # Specify the app you're interested in
    if app_name in catalogue['home']:
        app_data = catalogue['home'][app_name]
        version = app_data['latest_version']  # Use latest_version to read corresponding YAML files
        questions_data = read_yaml_file(app_name, version, 'questions.yaml')
        metadata_data = read_yaml_file(app_name, version, 'metadata.yaml')
        app_versions_data = generate_app_versions_data(app_data, questions_data, metadata_data)
        write_app_versions(app_versions_data)
        print(f"Data for {app_name} has been successfully written to app_versions.json")
    else:
        print(f"App {app_name} not found in catalogue.")

if __name__ == "__main__":
    main()
