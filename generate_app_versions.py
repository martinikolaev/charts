import json
import yaml
import os
import re
from datetime import datetime

RECREATE_ALL = True  # Control flag for recreating app_versions.json files

def read_catalog(filename='catalog.json'):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Catalog file {filename} not found.")
        return {}

def read_yaml_file(app_path, version, filename):
    yaml_file_path = os.path.join(app_path, version, filename)
    try:
        with open(yaml_file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"File {yaml_file_path} not found.")
        return {}

def list_all_apps(base_path='home'):
    try:
        return [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    except FileNotFoundError:
        print(f"Base directory {base_path} not found.")
        return []

def get_app_versions(app_path):
    try:
        version_dirs = [d for d in os.listdir(app_path) if os.path.isdir(os.path.join(app_path, d)) and re.match(r'^\d+\.\d+\.\d+$', d)]
        return sorted(version_dirs, key=lambda x: [int(part) for part in x.split('.')])
    except FileNotFoundError:
        print(f"App directory {app_path} not found.")
        return []

def generate_app_versions_data(app_name, app_path, version, catalog_data):
    questions_data = read_yaml_file(app_path, version, 'questions.yaml') or {}
    metadata_data = read_yaml_file(app_path, version, 'metadata.yaml') or {}

    # Process runAsContext to ensure gid and uid are integers, replace with 568 if not
    if "runAsContext" in metadata_data:
        for context in metadata_data["runAsContext"]:
            try:
                context["gid"] = int(context["gid"])
                context["uid"] = int(context["uid"])
            except (ValueError, TypeError):
                context["gid"] = 568
                context["uid"] = 568
    else:
        metadata_data["runAsContext"] = []

    app_data = catalog_data.get('home', {}).get(app_name, {})
    chart_metadata = {
        "name": app_data.get("name"),
        "description": app_data.get("description"),
        "annotations": {"title": app_data.get("title")},
        "type": "application",
        "version": version,
        "appVersion": app_data.get("latest_app_version", version),
        "kubeVersion": ">=1.16.0-0",
        "maintainers": app_data.get("maintainers", []),
        "home": app_data.get("home"),
        "icon": app_data.get("icon_url"),
        "sources": app_data.get("sources", []),
        "keywords": app_data.get("tags", [])
    }

    app_version_data = {
        "healthy": True,
        "supported": True,
        "healthy_error": None,
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "required_features": ["normalize/acl", "normalize/ixVolume"],
        "human_version": version,
        "version": version,
        "location": f"/__w/{app_path}/{version}",
        "app_readme": questions_data.get('app_readme', 'Default README content'),
        "detailed_readme": questions_data.get('detailed_readme', 'Default detailed README content'),
        "schema": {
            "groups": questions_data.get('groups', []),
            "portals": {},
            "questions": questions_data.get('questions', [])
        },
        "app_metadata": metadata_data,
        "chart_metadata": chart_metadata
    }
    return app_version_data

def process_apps(base_path='home', recreate_all=False):
    catalog_data = read_catalog()
    all_apps = list_all_apps(base_path)

    for app_name in all_apps:
        app_path = os.path.join(base_path, app_name)
        versions = get_app_versions(app_path)
        app_versions = {}

        for version in versions:
            if recreate_all or version not in app_versions:
                app_versions[version] = generate_app_versions_data(app_name, app_path, version, catalog_data)

        if app_versions:
            with open(os.path.join(app_path, 'app_versions.json'), 'w') as file:
                json.dump(app_versions, file, indent=4)
            print(f"Processed {app_name} with {len(versions)} versions.")

def main():
    process_apps(recreate_all=RECREATE_ALL)

if __name__ == "__main__":
    main()
