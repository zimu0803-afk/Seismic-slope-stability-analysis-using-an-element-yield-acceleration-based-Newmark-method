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
        print(f"文件 {file_path_template} 缺少必要列")
except FileNotFoundError:
    print(f"文件 {file_path_template} 未找到，请将输入文件放入 ./data 目录")
except Exception as e:
    print(f"读取文件时出错: {e}")

if data_list:
    final_df = pd.DataFrame(data_list, columns=["X", "Y", "r"])
    output_excel_path = os.path.join(output_dir, 'extracted_centers.xlsx')
    final_df.to_excel(output_excel_path, index=False)
    print(f"已成功保存 {len(final_df)} 行数据到 {output_excel_path}")