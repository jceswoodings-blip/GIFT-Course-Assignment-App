import pandas as pd

def get_csv_output(data: dict, output_file_path: str):
    # data_scores = [key for key, value in data.items()]
    # if not data_scores:
    #     exit("\nNo successful attempts within parameters. Please broaden parameters to increase sucsess chance")
    # print("\nAccepted average scores:  " + str(data_scores))

    # print(min(data_scores))
    output_df = pd.DataFrame(data)

    csv_out = output_df.to_csv(output_file_path, index=False)
    print("CSV Created")
    return csv_out