import pandas as pd
from pathlib import Path
import time
def Remove_last_names(name: str) -> str:
    name = str(name)
    name = name.strip()
    parts = name.split(" ")
    if parts[0].capitalize() == "Angus":
        parts[0] = "Gus"
    return f"{parts[0].capitalize()} {parts[1][0].upper()}" if len(parts) > 1 else parts[0].capitalize()

def Apply_format_to_each(df: pd.DataFrame) -> pd.DataFrame:
    df2 = {}
    for col_name, participants in df.items():
        participants = participants.tolist()
        value = list(map(Remove_last_names, participants))
        df2.update({col_name: value})
    df2 = pd.DataFrame(df2)
    df2 = df2.fillna(" ")
    return df2

def Get_source_path() -> str:
    source_path = ""
    while source_path == "" or source_path == " ":
        source_path = (input("Please paste the file path of the file you want to process here:")
                    .strip().replace("\"", ""))
    return source_path  


def main():
    source_path = Get_source_path()

    df = pd.read_csv(fr"{source_path}")
    df = df.fillna(" ")
    df2 = Apply_format_to_each(df)
    df2.columns = [" " if "Unnamed: " in course else course for course in df2.columns]
    df2.to_csv(Path.home()/'Desktop'/'First names only allocations GIFT.csv', index=False)
    print("New file created in your desktop, called \'First names only allocations GIFT\'"
          "\n This window will close after 5 seconds")
    time.sleep(5)
    
if __name__ == "__main__":
    main()

