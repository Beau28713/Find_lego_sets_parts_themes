import csv
import pandas as pd
import matplotlib.pyplot as plt
import requests
import gzip


def update_csv_files():
    url_colors = "https://cdn.rebrickable.com/media/downloads/colors.csv.gz"
    url_parts_cat = "https://cdn.rebrickable.com/media/downloads/part_categories.csv.gz"
    url_parts = "https://cdn.rebrickable.com/media/downloads/parts.csv.gz"
    url_sets = "https://cdn.rebrickable.com/media/downloads/sets.csv.gz"
    url_themes = "https://cdn.rebrickable.com/media/downloads//themes.csv.gz"

    download_colors = requests.get(url_colors, allow_redirects=True)
    download_parts_cat = requests.get(url_parts_cat, allow_redirects=True)
    download_parts = requests.get(url_parts, allow_redirects=True)
    download_sets = requests.get(url_sets, allow_redirects=True)
    download_themes = requests.get(url_themes, allow_redirects=True)

    with gzip.open("CSV_files\colors.csv.gz", "wb") as file_color, gzip.open(
        "CSV_files\part_categories.csv.gz", "wb"
    ) as file_part_cat, gzip.open(
        "CSV_files\parts.csv.gz", "wb"
    ) as file_parts, gzip.open(
        "CSV_files\sets.csv.gz", "wb"
    ) as file_sets, gzip.open(
        "CSV_files\\themes.csv.gz", "wb"
    ) as file_themes:
        file_color.write(download_colors.content)
        file_part_cat.write(download_parts_cat.content)
        file_parts.write(download_parts.content)
        file_sets.write(download_sets.content)
        file_themes.write(download_themes.content)

    with gzip.open("CSV_files\colors.csv.gz", "rb") as file_color, gzip.open(
        "CSV_files\part_categories.csv.gz", "rb"
    ) as file_part_cat, gzip.open(
        "CSV_files\parts.csv.gz", "rb"
    ) as file_parts, gzip.open(
        "CSV_files\sets.csv.gz", "rb"
    ) as file_sets, gzip.open(
        "CSV_files\\themes.csv.gz", "rb"
    ) as file_themes:
        color_byte = file_color.read()
        part_cat_byte = file_part_cat.read()
        parts_byte = file_parts.read()
        sets_byte = file_sets.read()
        themes_byte = file_themes.read()

    color = gzip.decompress(color_byte)
    part_cat = gzip.decompress(part_cat_byte)
    parts = gzip.decompress(parts_byte)
    sets = gzip.decompress(sets_byte)
    themes = gzip.decompress(themes_byte)

    with open("CSV_files\colors.csv", "wt", encoding="utf-8") as file_color, open(
        "CSV_files\part_categories.csv", "wt", encoding="utf-8"
    ) as file_part_cat, open(
        "CSV_files\parts.csv", "wt", encoding="utf-8"
    ) as file_parts, open(
        "CSV_files\sets.csv", "wt", encoding="utf-8"
    ) as file_sets, open(
        "CSV_files\\themes.csv", "wt", encoding="utf-8"
    ) as file_themes:
        file_color.write(color.decode())
        file_part_cat.write(part_cat.decode())
        file_parts.write(parts.decode())
        file_sets.write(sets.decode(encoding="UTF-8"))
        file_themes.write(themes.decode())


def get_db(database: str):
    return pd.read_csv(f"CSV_files\{database}.csv")


def is_missing_data(data_base: str):
    is_missing = get_db(data_base).isna().sum()
    print(is_missing)


def lego_colors_data(color: str):
    color_data = get_db("colors")
    print(color_data[color_data["name"] == color.title()].set_index("name"))


def get_sets_theme_data(theme_id: int = None, set_num: str = None):
    set_db = get_db("sets")
    theme_db = get_db("themes")

    if theme_id:

        print(theme_db[theme_db["id"] == theme_id].fillna("No data").set_index("id"))
        print("-----------------------------------")

    if set_num and not theme_id:
        set_by_set_num = set_db[set_db["set_num"] == set_num].set_index("set_num")
        if set_by_set_num.empty:
            print("Not in database")
        else:
            print(set_by_set_num)

    elif not set_num and theme_id:
        set_by_theme_id = set_db[set_db["theme_id"] == theme_id].set_index("set_num")

        for index, data in set_by_theme_id.iterrows():
            print(f"Set Numner {index}")
            print(data)
            print("--------------------------------")
    else:
        print("No Theme ID or Set Number was suppled")


def get_parts_data(part_num: str = None):
    try:
        if part_num:
            parts_db = get_db("parts")
            parts_cat_db = get_db("part_categories")

            part = parts_db[parts_db["part_num"] == part_num].set_index("part_num")

            part_cat = parts_cat_db[
                parts_cat_db["id"] == part.at[part_num, "part_cat_id"]
            ].set_index("id")

            print(part)
            print("-------------------")
            print(
                f"Part {part_num} is in category {part_cat.at[part.at[part_num, 'part_cat_id'], 'name']}"
            )
        else:
            print("No part number was supplied")

    except KeyError:
        print("Part not in database")


def main():
    # is_missing_data("themes")
    # lego_colors_data("Black")
    # get_sets_theme_data(theme_id=22)
    get_parts_data("003383")
    # update_csv_files()


if __name__ == "__main__":
    main()
