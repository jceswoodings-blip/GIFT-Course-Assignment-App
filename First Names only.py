import pandas as pd
from pathlib import Path
import time
def Remove_last_names(name):
    name = str(name)
    name = name.strip()
    parts = name.split(" ")
    if parts[0].capitalize() == "Angus":
        parts[0] = "Gus"
    return parts[0].capitalize()


path_to_use = ""
while path_to_use == "" or path_to_use == " ":
    path_to_use = (input("please paste the file path of the file you want to process here:")
                   .strip().replace("\"", ""))
df = pd.read_csv(fr"{path_to_use}")
df = df.fillna(" ")
df2 = {}

for col_name, value in df.items():
    value = value.tolist()
    value = list(map(Remove_last_names, value))
    df2.update({col_name: value})

df2 = pd.DataFrame(df2)
df2 = df2.fillna(" ")
df2.columns = [" " if "Unnamed: " in course else course for course in df2.columns]
df2.to_csv(Path.home()/'Desktop'/'First names only allocations GIFT.csv', index=False)
print("New file created in your desktop, called \'First names only allocations GIFT\'"
      "\n This window will close after 5 seconds")
time.sleep(5)

