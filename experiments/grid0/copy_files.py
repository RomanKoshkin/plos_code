import os, shutil
import pandas as pd

grid = pd.read_csv('grid.csv')

for i, cell in grid.iterrows():
    os.makedirs(f'cell_{i}', exist_ok=True)
    os.makedirs(f'cell_{i}/data', exist_ok=True)
    shutil.copy('dispatcher.py', f'cell_{i}')
    shutil.copy('run_cell.py', f'cell_{i}')
    shutil.copy('grid.csv', f'cell_{i}')
