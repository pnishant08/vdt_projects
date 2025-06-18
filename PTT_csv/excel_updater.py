import pandas as pd
import os

# Fixed path where the Excel will always be updated
FILE_PATH = "defect_logs/defect_log.xlsx"

def update_excel_file(upstream, orientation, width):
    """
    This function updates the Excel file at the fixed location with the new defect information.
    """

    if not os.path.exists(FILE_PATH):
        # If the file doesn't exist, create it with the required structure
        columns = ['Upstream', 'Orientation_1', 'Width_1', 'Orientation_2', 'Width_2',
                   'Orientation_3', 'Width_3', 'Orientation_4', 'Width_4', 'Orientation_5', 'Width_5']
        df = pd.DataFrame(columns=columns)
    else:
        df = pd.read_excel(FILE_PATH)

    if upstream in df['Upstream'].values:
        row_index = df[df['Upstream'] == upstream].index[0]
        col_pairs = [(col, col.replace('Orientation', 'Width')) for col in df.columns if 'Orientation' in col]

        for orientation_col, width_col in col_pairs:
            if pd.isna(df.at[row_index, orientation_col]):
                df.at[row_index, orientation_col] = orientation
                df.at[row_index, width_col] = width
                break
        else:
            print(f"No empty columns available for Upstream {upstream}.")
    else:
        new_row = {'Upstream': upstream, 'Orientation_1': orientation, 'Width_1': width}
        for i in range(2, 6):  # Extend if you need more Orientation-Width pairs
            new_row[f'Orientation_{i}'] = pd.NA
            new_row[f'Width_{i}'] = pd.NA

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    df.to_excel(FILE_PATH, index=False)
    print(f"Data successfully updated for Upstream {upstream} at {FILE_PATH}.")
