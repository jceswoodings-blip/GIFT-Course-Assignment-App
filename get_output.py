import pandas as pd

def get_csv_output(df_dict: dict, output_file_path: str):
    data_scores = [key for key, value in df_dict.items()]
    if not data_scores:
        exit("\nNo successful attempts within parameters. Please broaden parameters to increase sucsess chance")
    print("\nAccepted average scores:  " + str(data_scores))

    print(min(data_scores))
    output_df = pd.DataFrame(df_dict[min(data_scores)])

    csv_out = output_df.to_csv(output_file_path, index=False)
    print("CSV Created")
    return csv_out