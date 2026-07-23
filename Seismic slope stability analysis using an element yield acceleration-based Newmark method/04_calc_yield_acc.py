import os
import subprocess
import pandas as pd
import xml.etree.ElementTree as ET

output_dir = "./output"
os.makedirs(output_dir, exist_ok=True)

# 请根据你的 GeoStudio 模版位置配置相对路径
BAT_PATH = "./geostudio_files/run_geostudio.bat"
XML_PATH = "./geostudio_files/slope_analysis.xml"
CSV_PATH = "./geostudio_files/SLOPE&3W Analysis/001/slip_surface.csv"

TARGET = 1.0
TOLERANCE = 0.01
MAX_ITER = 10

results = []

for n in range(27):
    def run_bat():
        if not os.path.exists(BAT_PATH):
            print(f"提示: 未检测到批处理脚本 {BAT_PATH}，如在实际工作中请部署相应 GeoStudio .bat 文件。")
            return
        with subprocess.Popen(['cmd.exe', '/c', BAT_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='gbk', errors='ignore') as process:
            try:
                for line in iter(process.stdout.readline, ''):
                    if "...solve complete." in line:
                        process.terminate()
                        break
            finally:
                process.stdout.close()
                process.stderr.close()

    def update_seismic(value):
        if not os.path.exists(XML_PATH):
            return
        tree = ET.parse(XML_PATH)
        root = tree.getroot()
        for elem in root.iter('Seismic Load'):
            if 'Horizontal' in elem.attrib:
                elem.set('Horizontal', f"{value:.3f}")
                break
        tree.write(XML_PATH, encoding='utf-8', xml_declaration=True)

    def get_fos():
        try:
            data = pd.read_csv(CSV_PATH)
            return float(data.iloc[n, 1])
        except Exception:
            return None

    update_seismic(0.0)
    run_bat()
    fos_initial = get_fos()

    if fos_initial is None:
        continue

    history = [(0.0, fos_initial)]
    if abs(fos_initial - TARGET) <= TOLERANCE:
        results.append({'滑面编号': n + 1, '地震系数': 0.0, '安全系数': round(fos_initial, 3)})
        continue

    if fos_initial < 2:
        low, high = 0.0, 0.6
    elif 2 <= fos_initial <= 2.9:
        low, high = 0.3, 0.8
    elif 2.9 <= fos_initial <= 4:
        low, high = 0.3, 1.5
    elif 4 <= fos_initial <= 5.5:
        low, high = 0.5, 3.0
    else:
        low, high = 0.5, 8

    converged = False
    for iter_count in range(MAX_ITER):
        mid = (low + high) / 2
        update_seismic(mid)
        run_bat()
        damn = get_fos()
        if damn is None:
            break
        history.append((mid, damn))
        if abs(damn - TARGET) < TOLERANCE:
            converged = True
            break
        if damn > TARGET:
            low = mid
        else:
            high = mid

    final_seismic, final_fos = history[-1]
    results.append({'滑面编号': n + 1, '地震系数': round(final_seismic, 3), '安全系数': round(final_fos, 3)})

if results:
    df = pd.DataFrame(results)[['滑面编号', '地震系数', '安全系数']]
    excel_path = os.path.join(output_dir, "convergence_results.xlsx")
    df.to_excel(excel_path, index=False)
    print(f"计算完成，结果已保存至: {excel_path}")