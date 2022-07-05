"""Used to search the active Lego's database by:
1. Updating your local dataframe.
2. Geting information on diffrent lego colors.
3. Finding out if any dataframe is missing data
4. Geting information on all the sets and themes Lego uses. 
5. Geting information on the many different parts lego has in stock

"""
import pandas as pd
import requests
import gzip
import typer

app = typer.Typer()


@app.command()
def update_csv_files():
    """Downloads the updated CSV files in a zip folder formate
    Saves the files, Then unzipes them and updates the CSV files
    """
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


def get_df(dataframe: str):
    """Helper Function that creates the rquired dataframes

    Args:
        dataframe (str): _description_

    Returns:
        Dataframe: Returns he required dataframe
    """
    return pd.read_csv(f"CSV_files\{dataframe}.csv")


@app.command()
def is_missing_data(
    dataframe: str = typer.Option(..., help="CSV file name to use", prompt=True)
):
    """Searches the desired dataframe for missing data "NA"

    Args:
        dataframe (str, Required): Name of the dataframe to search
    """
    is_missing = get_df(dataframe).isna().sum()
    print(is_missing)


@app.command()
def lego_colors_data(
    color: str = typer.Option(..., help="Color you would like to look up", prompt=True)
):
    """Get information on the different colors used by Lego

    Args:
        color (str, Required):Color you wish to search for.
    """
    color_data = get_df("colors")
    print(color_data[color_data["name"] == color.title()].set_index("name"))


@app.command()
def get_sets_theme_data(
    theme_id: int = typer.Option(
        ..., help="Theme id number you want to search", prompt=True
    ),
    set_num: str = typer.Option(
        None, help="Set number you wish to search"
    ),
):
    """Get the informaton on themes and sets.

    Args:
        theme_id (int, Required): Theme ID number youu wish to search for.
        set_num (str, Optional): Set number you wish to search for.
    """
    set_db = get_df("sets")
    theme_db = get_df("themes")

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


@app.command()
def get_parts_data(part_num: str = typer.Option(..., help="Part number you wish to search", prompt=True)):
    """Search for Lego parts 

    Args:
        part_num (str, Required): Part number you wish to search for.
    """
    try:
        if part_num:
            parts_db = get_df("parts")
            parts_cat_db = get_df("part_categories")

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


if __name__ == "__main__":
    app()
