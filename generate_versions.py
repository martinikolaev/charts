import json
import yaml
import os
import re
from datetime import datetime

def read_catalog(filename='catalog.json'):
    """Reads the catalog file and returns its content as a dictionary."""
    with open(filename, 'r') as file:
        return json.load(file)

def read_yaml_file(app_name, version, filename):
    """Reads a YAML file for the given app version and returns its content."""
    yaml_file_path = os.path.join('home', app_name, version, filename)
    try:
        with open(yaml_file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"File {yaml_file_path} not found.")
        return {}

def is_version_directory(dirname):
    """Checks if a directory name matches a version pattern."""
    pattern = re.compile(r'^\d+\.\d+\.\d+$')
    return pattern.match(dirname) is not None

def get_app_versions(app_name):
    """Lists all version directories under the home/app_name path."""
    versions_path = os.path.join('home', app_name)
    try:
        version_dirs = [d for d in os.listdir(versions_path) if os.path.isdir(os.path.join(versions_path, d)) and is_version_directory(d)]
        return sorted(version_dirs, key=lambda x: [int(part) for part in x.split('.')])  # Sorting versions properly
    except FileNotFoundError:
        print(f"Directory {versions_path} not found.")
        return []

def generate_app_versions_data(app_name, version):
    """Generates app_versions data for a specific version."""
    questions_data = read_yaml_file(app_name, version, 'questions.yaml')
    metadata_data = read_yaml_file(app_name, version, 'metadata.yaml')
    
    # Ensure gid and uid are always 568 in runAsContext
    for context in metadata_data.get("runAsContext", []):
        context["gid"] = 568
        context["uid"] = 568

    location = f"/__w/home/{app_name}/{version}"

    return {
        "healthy": True,
        "supported": True,
        "healthy_error": None,
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
            # This section might need adjustments to pull data from the correct source
            "name": app_name,
            "description": "A description",  # Placeholder
            "annotations": {"title": app_name},
            "type": "application",
            "version": version,
            "appVersion": version,
            "kubeVersion": ">=1.16.0-0",
            "maintainers": [{"name": "maintainer name", "email": "email@example.com"}],  # Placeholder
            "home": "http://example.com",  # Placeholder
            "icon": "http://example.com/icon.png",  # Placeholder
            "sources": ["http://example.com/source"]  # Placeholder
        }
    }

def write_app_versions(app_versions, filename='app_versions.json'):
    """Writes the app versions data to a file."""
    with open(filename, 'w') as file:
        json.dump(app_versions, file, indent=4)

def main():
    app_name = 'idractool'  # Example app name
    app_versions = {}

    for version in get_app_versions(app_name):
        app_version_data = generate_app_versions_data(app_name, version)
        app_versions[version] = app_version_data
    
    if app_versions:
        write_app_versions(app_versions)
        print(f"Data for {app_name} has been successfully compiled into {app_name}_versions.json")
    else:
        print(f"No version data found for {app_name}.")

if __name__ == "__main__":
    main()
