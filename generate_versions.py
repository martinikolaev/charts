import json
import yaml  # PyYAML library
from datetime import datetime
import os

def read_catalog(filename='catalog.json'):
    """Reads the catalog file and returns its content as a dictionary."""
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
    Takes the application data extracted from the catalog, the questions data, and the metadata data,
    and generates the structure for app_versions.json with dynamic and static values for specified fields.
    """
    latest_version = app_data['latest_version']
    # Dynamically construct the 'location' field
    location = f"/__w/home/{app_name}/{latest_version}"
    
    # Adjust runAsContext in metadata_data to ensure gid and uid are always 568
    adjusted_runAsContext = []
    for context in metadata_data.get("runAsContext", []):
        context["gid"] = 568
        context["uid"] = 568
        adjusted_runAsContext.append(context)
    metadata_data["runAsContext"] = adjusted_runAsContext

    app_versions_data = {
        latest_version: {
            "healthy": True,
            "supported": True,
            "healthy_error": None,
            "last_update": "2024-02-03 10:49:45",
            "required_features": ["normalize/acl", "normalize/ixVolume"],
            "human_version": latest_version,
            "version": latest_version,
            "location": location,  # Set the dynamically generated location
            "app_readme": app_data.get('app_readme', ''),
            "detailed_readme": app_data.get('app_readme', ''),
            "schema": {
                "groups": questions_data.get('groups', []),
                "portals": {},
                "questions": questions_data.get('questions', [])
            },
            "app_metadata": metadata_data,
            "chart_metadata": {
                "name": app_data.get("name", ""),
                "description": app_data.get("description", ""),
                "annotations": {
                    "title": app_data.get("name", "")  # Assuming title comes from the name field
                },
                "type": "application",
                "version": latest_version,
                "appVersion": latest_version,
                "kubeVersion": ">=1.16.0-0",
                "maintainers": app_data.get("maintainers", []),
                "home": app_data.get("home", ""),
                "icon": app_data.get("icon_url", ""),
                "sources": app_data.get("sources", [])
            }
        }
    }
    return app_versions_data

def write_app_versions(app_versions_data, filename='app_versions.json'):
    """Writes the app versions data to a file."""
    with open(filename, 'w') as file:
        json.dump(app_versions_data, file, indent=4)

def main():
    global app_name
    catalog = read_catalog()  # Reads the catalog.json file
    app_name = 'idractool'  # Specify the app you're interested in
    if app_name in catalog['home']:
        app_data = catalog['home'][app_name]
        version = app_data['latest_version']  # Use latest_version to read corresponding YAML files
        questions_data = read_yaml_file(app_name, version, 'questions.yaml')
        metadata_data = read_yaml_file(app_name, version, 'metadata.yaml')
        app_versions_data = generate_app_versions_data(app_data, questions_data, metadata_data)
        write_app_versions(app_versions_data)
        print(f"Data for {app_name} has been successfully written to app_versions.json")
    else:
        print(f"App {app_name} not found in catalog.")

if __name__ == "__main__":
    main()
