import os
import numpy as np

dt = 0.02
n1 = 1
dt1 = dt / n1

data_dir = "./data"
output_dir = "./output"
os.makedirs(output_dir, exist_ok=True)

ei_path = os.path.join(data_dir, 'EI.txt')
ky_path = os.path.join(data_dir, '1.txt')
out_path = os.path.join(output_dir, 'displacement_results.txt')

if not os.path.exists(ei_path) or not os.path.exists(ky_path):
    print(f"Error: Unable to find {ei_path} or {ky_path}. Please ensure they are placed in ./data directory.")
else:
    with open(ei_path, 'r') as f:
        ear = [float(line.strip()) for line in f.readlines()]

    with open(ky_path, 'r') as f:
        ky_list = [float(line.strip()) for line in f.readlines()[:122169]]

    with open(out_path, 'w') as f_out:
        for ky in ky_list:
            vel0 = 0.0
            disp = 0.0
            max_i = min(1500 * n1, len(ear) - 1)
            for i in range(max_i):
                ac1 = ear[i]
                ac2 = ear[i + 1]
                ac = 0.5 * ac1 + 0.5 * ac2
                da = ac - ky

                if da >= 1e-5:
                    vel1 = vel0
                    vel2 = vel1 + da * dt1
                    disp += (vel1 + vel2) * dt1 * 0.5
                    vel0 = vel2
                else:
                    vel3 = vel0 + da * dt1
                    if vel3 >= 1e-5:
                        vel1 = vel0
                        vel2 = vel3
                        disp += (vel1 + vel2) * dt1 * 0.5
                        vel0 = vel2
                    else:
                        vel1 = vel0
                        vel2 = 0.0
                        disp += (vel1 + vel2) * dt1 * 0.5
                        vel0 = vel2

            f_out.write(f"{disp}\n")

    print(f"Displacement integration completed. Results saved to {out_path}")