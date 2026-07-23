import os
import pandas as pd

output_dir = "./output"
os.makedirs(output_dir, exist_ok=True)

data_list = []
global_row = 1

# 请将此处的 csv 路径指向你的 GeoStudio 导出文件目录
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
            print(f"文件 {file_path} 缺少 'X' 或 'Y' 列，跳过")
    except FileNotFoundError:
        pass  # 不存在的文件自动跳过
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")

if data_list:
    final_df = pd.DataFrame(data_list, columns=["FullySpecifiedSlips ID", "Point ID", "X", "Y"])
    output_excel_path = os.path.join(output_dir, 'slip_points.xlsx')
    final_df.to_excel(output_excel_path, index=False)
    print(f"已成功保存 {len(final_df)} 行数据到 {output_excel_path}")
else:
    print("未发现有效 csv 文件，请检查输入目录。")
