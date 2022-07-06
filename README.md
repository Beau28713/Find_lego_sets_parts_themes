# Description   
Use Typer, Pandas, and Gzip libraries to implement an easy to use command line  
interface that allows you to search the official legos database for Sets, parts, and themes of lego's. 

Click [here](https://rebrickable.com/downloads/) to manually download the lego CSV files used in this project. 

# How to use
## Use --help or pydoc to get general information.

```
(DataCamp) C:\Users\beau2\Code\Python\Lego_bricks>python main.py --help
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.
  --help                Show this message and exit.

Commands:
  get-parts-data       Search for Lego parts
  get-sets-theme-data  Get the informaton on themes and sets.
  is-missing-data      Searches the desired dataframe for missing data "NA"
  lego-colors-data     Get information on the different colors used by Lego
  update-csv-files     Downloads the updated CSV files in a zip folder...
```
```
(DataCamp) C:\Users\beau2\Code\Python\Lego_bricks>pydoc main
Help on module main:

NAME
    main

DESCRIPTION
    Used to search the active Lego's database by:
    1. Updating your local dataframe.
    2. Geting information on diffrent lego colors.
    3. Finding out if any dataframe is missing data
    4. Geting information on all the sets and themes Lego uses.
    5. Geting information on the many different parts lego has in stock

FUNCTIONS
    get_df(dataframe: str)
        Helper Function that creates the rquired dataframes

        Args:
            dataframe (str): _description_

        Returns:
            Dataframe: Returns he required dataframe

    get_parts_data(part_num: str = <typer.models.OptionInfo object at 0x0000023E1FA27670>)
        Search for Lego parts

        Args:
            part_num (str, Required): Part number you wish to search for.

    get_sets_theme_data(theme_id: int = <typer.models.OptionInfo object at 0x0000023E1FA275E0>, set_num: str = <typer.models.OptionInfo object at 0x0000023E1FA27610>)
        Get the informaton on themes and sets.

        Args:
            theme_id (int, Required): Theme ID number youu wish to search for.
            set_num (str, Optional): Set number you wish to search for.

    is_missing_data(dataframe: str = <typer.models.OptionInfo object at 0x0000023E1FA27520>)
        Searches the desired dataframe for missing data "NA"

        Args:
            dataframe (str, Required): Name of the dataframe to search

    lego_colors_data(color: str = <typer.models.OptionInfo object at 0x0000023E1FA27580>)
        Get information on the different colors used by Lego

        Args:
            color (str, Required):Color you wish to search for.

    update_csv_files()
        Downloads the updated CSV files in a zip folder formate
        Saves the files, Then unzipes them and updates the CSV files

DATA
    app = <typer.main.Typer object>

FILE
    c:\users\beau2\code\python\lego_bricks\main.py
```
## Get help on individual functions
```
(DataCamp) C:\Users\beau2\Code\Python\Lego_bricks>python main.py get-sets-theme-data --help
Usage: main.py get-sets-theme-data [OPTIONS]

  Get the informaton on themes and sets.

  Args:     theme_id (int, Required): Theme ID number you wish to search for.
  set_num (str, Optional): Set number you wish to search for.

Options:
  --theme-id INTEGER  Theme id number you want to search  [required]
  --set-num TEXT      Set number you wish to search
  --help              Show this message and exit.
```
## Requirements
pandas==1.4.2  
requests==2.28.1  
typer==0.4.2