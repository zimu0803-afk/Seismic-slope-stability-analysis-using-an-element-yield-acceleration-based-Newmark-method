import os
import pandas as pd

output_dir = "./output"
os.makedirs(output_dir, exist_ok=True)

data_list = []
global_row = 1

# Path template for GeoStudio output files
file_path_template = './data/geostudio_output/slice_{}.csv'

for file in range(1, 3000):
    file_path = file_path_template.format(file)
    try:
        df = pd.read_csv(file_path)
        if 'X' in df.columns and 'Y' in df.columns:
            x_values = df['X'].tolist()
            y_values = df['Y'].tolist()
            for x_val, y_val in zip(x_values, y_values):
                data_list.append([file, global_row, x_val, y_val])
                global_row += 1
        else:
            print(f"File {file_path} missing 'X' or 'Y' columns. Skipped.")
    except FileNotFoundError:
        pass  # Automatically skip non-existent files
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")

if data_list:
    final_df = pd.DataFrame(data_list, columns=["FullySpecifiedSlips ID", "Point ID", "X", "Y"])
    output_excel_path = os.path.join(output_dir, 'slip_points.xlsx')
    final_df.to_excel(output_excel_path, index=False)
    print(f"Successfully saved {len(final_df)} rows of data to {output_excel_path}")
else:
    print("No valid CSV files found. Please check input directory.")