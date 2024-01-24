import copy
import csv
import json

BASE_DATA_PATH = "./data/"
BASE_API_PATH = "./api/v1/"

def get_csv(csv_filename, key_column = None):
    if key_column is not None:
        return get_csv_as_dict(csv_filename, key_column)
    return get_csv_as_list(csv_filename)

def get_csv_as_dict(csv_filename, key_column = None):
    data = {}
    with open(f"{BASE_DATA_PATH}{csv_filename}", encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        for rows in csvReader:
            key = rows[key_column]
            data[key] = rows
    return data

def get_csv_as_list(csv_filename):
    data = []
    with open(f"{BASE_DATA_PATH}{csv_filename}", encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        for rows in csvReader:
            data.append(rows)
    return data

def write_dict_to_json(data, json_filename):
    with open(f"{BASE_API_PATH}{json_filename}", 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))

def update_runs_and_runners():
    runs = get_csv_as_dict("runs.csv", "run_uuid")
    runners = get_csv_as_dict("runners.csv", "runner_uuid")

    # Deepcopy needed to prevent circular import when appending the "runners" and "runs" lists.
    runs_copy = copy.deepcopy(runs)
    runners_copy = copy.deepcopy(runners)

    runs_to_runners = get_csv_as_list("runs_to_runners.csv")

    # Append list of runner objects to each run object.
    for entry in runs_to_runners:
        if "runners" not in runs[entry["run_uuid"]]:
            runs[entry["run_uuid"]]["runners"] = [runners_copy[entry["runner_uuid"]]]
        else:
            runs[entry["run_uuid"]]["runners"].append(runners_copy[entry["runner_uuid"]])

    # Append list of run objects to each runner object.
    for entry in runs_to_runners:
        if "runs" not in runners[entry["runner_uuid"]]:
            runners[entry["runner_uuid"]]["runs"] = [runs_copy[entry["run_uuid"]]]
        else:
            runners[entry["runner_uuid"]]["runs"].append(runs_copy[entry["run_uuid"]])

    write_dict_to_json(runs, "runs.json")
    write_dict_to_json(runners, "runners.json")

def update_categories():
    write_dict_to_json(
        get_csv_as_dict("categories.csv", "category_uuid"),
        "categories.json"
    )


if __name__ == "__main__":
    update_runs_and_runners()
    update_categories()
