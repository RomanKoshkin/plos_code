import os, time
import subprocess
import numpy as np
import copy, sys
import pandas as pd
import pickle

MAX_PROCESSES = 28
grid = pd.read_csv('grid.csv')
num_cells = grid.shape[0]


def check_running(PROC):
    C = np.zeros((num_cells,))
    for i, proc in enumerate(PROC):
        if proc.poll() != 0:
            C[i] = 1
    sys.stdout.write(str(C.astype(int)))
    sys.stdout.flush()
    sys.stdout.write("\b" * len(str(C)))
    return C.sum()


PROC = []
for cell_id in range(num_cells):
    PROC.append(subprocess.Popen(
        ['python', 'run_cell.py', str(cell_id)],
        cwd=f'cell_{cell_id}',
    ))
    while check_running(PROC) > MAX_PROCESSES:
        time.sleep(4)

print('exited')