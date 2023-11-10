import sys
import os
import json
import csv


# Finds and adds all the repositories in the directory and returns it as a list.
def get_all_subdirectories(path: str) -> [str]:
    subdirectories_path = []
    for x in next(os.walk(path))[1]:
        subdirectories_path.append(path + "/" + x)
    return subdirectories_path


# When the files are in a subdirectory inside the repository, the path will have '\\' instead of '/'.
# This function then replaces every instance of it, and makes the code look cleaner.
def edit_path(path: str) -> str:
    return path.replace("\\", "/")


# Gets all the requirements.txt and package.json paths in a subdirectory
def get_files(directory_path: str) -> [str]:
    temp = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file == "requirements.txt":
                temp.append(edit_path(root) + "/" + file)
            elif file == "package.json":
                temp.append(edit_path(root) + "/" + file)
    return temp


# Creates and saves a csv file with the list of dependencies at the root path.
def save_dependencies_csv(dependencies: list, path: str):
    path = path + "/sbom.csv"
    with open(path, "w", encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        for data in dependencies:
            writer.writerow(data)
    print(f"Saved SBOM in CSV format to '{path}'")


# Creates and saves a json file with the list of dependencies at the root path.
def save_dependencies_json(dependencies: list, path: str):
    path = path + "/sbom.json"
    temp_dict = {"npm": {}, "pip": {}}
    for name, version, type_temp, file_path in dependencies:
        if file_path not in temp_dict[type_temp]:
            temp_dict[type_temp][file_path] = {}
        temp_dict[type_temp][file_path][name] = version
    json_object = json.dumps(temp_dict, indent=4)
    with open(path, "w") as f:
        f.write(json_object)
    print(f"Saved SBOM in JSON format to '{path}'")


# Takes in a list of file paths to all the .txt and .json files.
# Returns a list of tuples with the name, version, type and file path of the dependency.
def import_dependencies(file_paths: list) -> list:
    dependencies = []
    type_temp = "npm"
    for file_path in file_paths:
        if file_path[-1] == "t":
            type_temp = "pip"
        with open(file_path, "r") as f:
            if type_temp == "pip":
                for line in f:
                    line = line.split("==")
                    dependencies.append((line[0], line[1].strip(), type_temp, file_path))
            else:
                data = json.load(f)
                for name, version in data["dependencies"].items():
                    dependencies.append((name, version, type_temp, file_path))
                for name, version in data["devDependencies"].items():
                    temp = (name, version, type_temp, file_path)
                    if temp in dependencies:
                        continue
                    dependencies.append(temp)
    return dependencies


def main():
    main_path = sys.argv[1]
    if main_path[-1] == "/":
        main_path = main_path[:-1]

    # StopIteration is a cause of the path not existing, so this try-except will catch that,
    # when trying to get all the subdirectories.
    try:
        subdirectories = get_all_subdirectories(main_path)
    except StopIteration:
        print("The path does not exist, try a different path")
        sys.exit()
    print(f"Found {len(subdirectories)} repositories in '{main_path}'")
    if len(subdirectories) == 0:
        print(f'No repositories to be found')
        sys.exit()

    # Gets all the requirements.txt and package.json, and stores it in files as a list.
    files = []
    for x in subdirectories:
        files.extend(get_files(x))

    dependencies = import_dependencies(files)

    # Creates and saves the sbom.csv and sbom.json files at the root path
    save_dependencies_csv(dependencies, main_path)
    save_dependencies_json(dependencies, main_path)


if __name__ == "__main__":
    main()
