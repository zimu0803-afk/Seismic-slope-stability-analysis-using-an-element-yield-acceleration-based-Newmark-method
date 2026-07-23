import os
import pandas as pd


def read_input_data(node_file, slip_surface_file):
    if not os.path.exists(node_file):
        raise FileNotFoundError(f"Node file does not exist: {node_file}")
    df_nodes = pd.read_excel(node_file, engine='openpyxl')
    df_nodes.columns = df_nodes.columns.str.strip().str.lower()

    if not os.path.exists(slip_surface_file):
        raise FileNotFoundError(f"Slip surface file does not exist: {slip_surface_file}")
    df_slips = pd.read_excel(slip_surface_file, engine='openpyxl')
    df_slips.columns = df_slips.columns.str.strip().str.lower()

    slip_surfaces = [
        {'x0': float(row['x0']), 'y0': float(row['y0']), 'r': float(row['r']), 'ay': float(row['ay'])}
        for _, row in df_slips.iterrows()
    ]
    return list(df_nodes[['x', 'y']].itertuples(index=False, name=None)), slip_surfaces


def assign_yield_acceleration(nodes, slip_surfaces):
    results = {}
    for x, y in nodes:
        min_ay = None
        for surface in slip_surfaces:
            dx = x - surface['x0']
            dy = y - surface['y0']
            if dx ** 2 + dy ** 2 <= surface['r'] ** 2:
                current_ay = surface['ay']
                min_ay = current_ay if (min_ay is None) else min(min_ay, current_ay)
        results[(x, y)] = min_ay if min_ay is not None else 10000.0
    return results


def save_results(results, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = pd.DataFrame([{"x": x, "y": y, "ay": ay} for (x, y), ay in results.items()])
    df.to_excel(output_path, index=False, engine='openpyxl')
    print(f"Results file saved to: {os.path.abspath(output_path)}")


if __name__ == "__main__":
    BASE_DIR = "./data"
    OUTPUT_DIR = "./output"

    NODE_FILE = os.path.join(BASE_DIR, "nodes.xlsx")
    SLIP_FILE = os.path.join(BASE_DIR, "slip_surfaces.xlsx")
    OUTPUT_FILE = os.path.join(OUTPUT_DIR, "assigned_yield_acc_results.xlsx")

    try:
        nodes, slip_surfaces = read_input_data(NODE_FILE, SLIP_FILE)
        results = assign_yield_acceleration(nodes, slip_surfaces)
        save_results(results, OUTPUT_FILE)
    except Exception as e:
        print(f"\nProcessing skipped or failed: {str(e)}")
        print(
            "Please ensure that input node file (nodes.xlsx) and slip surface file (slip_surfaces.xlsx) are placed in ./data directory.")