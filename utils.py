import os
import argparse
import json
import pandas as pd


def remove_duplicate_csv_common(path=None, field=None):
    try:
        name_list = []
        link_list = []
        duplicate_data = {}
        df = pd.read_csv(path)
        df_dict = df.to_dict()
        no_of_entries = len(df_dict[field])
        for i in range(no_of_entries):
            name = df_dict[field][i]
            link = df_dict["Link"][i]
            if name not in name_list:
                name_list.append(name)
                link_list.append(link)
            else:
                duplicate_data[name] = link
        rows_unique = pd.DataFrame({"Name": name_list, "Link": link_list})
        rows_duplicate = pd.DataFrame(
            {"Name": list(duplicate_data.keys()), "Link": list(duplicate_data.values())}
        )

        path_list = path.split("/")[:-1]
        file_name = path.split("/")[-1]

        duplicate_path = "/".join(path_list) + "/" + "duplicate"
        unique_path = "/".join(path_list) + "/" + "unique"

        os.makedirs(unique_path, exist_ok=True)
        os.makedirs(duplicate_path, exist_ok=True)

        duplicate_path = duplicate_path + "/" + file_name
        unique_path = unique_path + "/" + file_name

        rows_duplicate.to_csv(duplicate_path, index=False)
        rows_unique.to_csv(unique_path, index=False)

    except Exception as e: 
        print("here")
        print(e)


# parser = argparse.ArgumentParser()
# parser.add_argument("-path", "--path", help="Path of the CSV", required=True)
# parser.add_argument(
#     "-field",
#     "--field",
#     default="Name",
#     help="Field you want to check for duplicate",
#     required=True,
# )

# args = parser.parse_args()

# input_path = args.path
# field = args.field

# remove_duplicate_csv_common(input_path, field)
