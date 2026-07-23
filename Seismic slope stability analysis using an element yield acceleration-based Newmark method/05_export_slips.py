import os
import pandas as pd

output_dir = "./output"
os.makedirs(output_dir, exist_ok=True)

file_path_template = './data/slip_surface.csv'
data_list = []

try:
    df = pd.read_csv(file_path_template)
    if 'SlipCenterX' in df.columns and 'SlipCenterY' in df.columns:
        x_values = df['SlipCenterX'].tolist()
        y_values = df['SlipCenterY'].tolist()
        r_values = df['SlipRadius'].tolist()
        for x_val, y_val, r_val in zip(x_values, y_values, r_values):
            data_list.append([x_val, y_val, r_val])
    else:
        print(f"File {file_path_template} missing required columns.")
except FileNotFoundError:
    print(f"File {file_path_template} not found. Please place input file in ./data directory.")
except Exception as e:
    print(f"Error reading file: {e}")

if data_list:
    final_df = pd.DataFrame(data_list, columns=["X", "Y", "r"])
    output_excel_path = os.path.join(output_dir, 'extracted_centers.xlsx')
    final_df.to_excel(output_excel_path, index=False)
    print(f"Successfully saved {len(final_df)} rows of data to {output_excel_path}")