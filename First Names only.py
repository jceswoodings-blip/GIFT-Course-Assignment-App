import pandas as pd
from pathlib import Path
import time
def Remove_last_names(name: str) -> str:
    # Given a full name, return only the first name and the initial of the last name
    name = str(name)
    name = name.strip()
    parts = name.split(" ")
    if parts[0].capitalize() == "Angus":
        parts[0] = "Gus"
    return f"{parts[0].capitalize()}" if len(parts) > 1 else parts[0].capitalize() # {parts[1][0].upper()}

def Apply_format_to_df(df: pd.DataFrame) -> pd.DataFrame:
    # iterate over each df column and map the Remove_last_names function to each value (list of participants)
    df2 = {}
    for col_name, participants in df.items():
        participants = participants.tolist()
        value = list(map(Remove_last_names, participants))
        df2.update({col_name: value})
    df2 = pd.DataFrame(df2)
    df2 = df2.fillna(" ")
    return df2

def Get_source_path() -> str:
    # Keep asking for file path until a valid one is provided (exists and is .csv)
    source_path = ""
    is_path_valid = False
    
    while is_path_valid == False:
        source_path = (input("Please paste the file path of the file you want to process here:")
                    .strip().replace("\"", ""))
        if Path(source_path).is_file() and Path(source_path).suffix == ".csv":
            is_path_valid = True
        elif Path(source_path).is_file() and Path(source_path).suffix != ".csv":
            print("The file you have provided is not a .csv file, please try again.")
        else:
            print("File path is not correct, please try again.")
    return source_path  


def main():
    source_path = Get_source_path()

    df = pd.read_csv(fr"{source_path}")
    df = df.fillna(" ")
    df2 = Apply_format_to_df(df)
    df2.columns = [" " if "Unnamed: " in course else course for course in df2.columns]
    df2.to_csv(Path.home()/'Desktop'/'First names only allocations GIFT.csv', index=False)
    print()
    print("New file created in your desktop, called \'First names only allocations GIFT\'"
          "\n This window will close after 5 seconds")
    time.sleep(5)
    
if __name__ == "__main__":
    main()

