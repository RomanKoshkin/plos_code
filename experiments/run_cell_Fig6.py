# NOTE: make sure to use `engine='python'` if you use `pandas.read_csv`
#
import numpy as np  # import pandas as pd

# np.random.seed(42)
print('<<<<<<<<<<<<<< **** NOT USING SEED **** >>>>>>>>>>>>>')

import os, sys, warnings
from pprint import pprint

sys.path.append('../')
print(f'PID: {os.getpid()}')

from modules_pybind.python_wrapper import Model  # here will wrap the c++ object with Python

from modules.utils import *
from modules.constants import ROOT

warnings.filterwarnings("ignore")

# --------------------------------------------------------------------------------------------------

grid = pd.read_csv('grid_Fig6.csv', engine='python')

cell_id = int(sys.argv[1])

print(f"cell_id: {cell_id}")

HAGA = bool(grid.iloc[cell_id].HAGA)  #True
astro = bool(grid.iloc[cell_id].astro)  #True
symmetric = bool(grid.iloc[cell_id].symmetric)  #True
Cp = float(grid.iloc[cell_id].Cp)  #True
Cd = float(grid.iloc[cell_id].Cd)  #True
taustf = float(grid.iloc[cell_id].taustf)  #True
taustd = float(grid.iloc[cell_id].taustd)  #True
repetition = int(grid.iloc[cell_id].repetition)  #True

t_sham_pre = int(grid.iloc[cell_id].t_sham_pre)
t_perturb = int(grid.iloc[cell_id].t_perturb)
n_perturb = int(grid.iloc[cell_id].n_perturb)
t_sham_post = int(grid.iloc[cell_id].t_sham_post)

# --------------------------------------------------------------------------------------------------

patternLenMs = 20
nass = 20

g = pd.read_csv('grid_Fig5a.csv')  # NOTE: get the grid5a based on which the models were run and checkpointed
ID = g[(g.astro == astro) & (g.HAGA == HAGA)].index.item()

# NOTE: we don't need to set
# - frozens, dump_dw, stp_on_I, UU, soft_clip_dw
m = Model.from_state(ID, path="data_Fig5a/states")  # NOTE: Fig5a is where we get the states from
NE = m.getState().NE
datafolder = "data_Fig6"
m.m.datafolder = datafolder

stimulator = Stimulator(
    m,
    stim_strength=1.0,
    nass=nass,
    rotate_every_ms=patternLenMs,
    cell_id=cell_id,
    dump_stats=1000,
    dumpfolder=datafolder,
)

cprint(f'HAGA: {HAGA} | astro: {astro} | mean(UU): {np.mean(m.getUU()[:NE]):.5f}', color='cyan', attrs=['bold'])

# NOTE: clusterize_=True saves .npy snapshots. Load them with SnapshotLoader
stimulator.sham(t_sham_pre, plasticity=False, clusterize_=True, saveFD=False)
# stimulator.perturb(t_perturb, stID=0, enID=100, plasticity=True, clusterize_=False, callback=None, saveFD=False)
stimulator.perturb_randM(t_perturb, M=n_perturb, plasticity=True, clusterize_=True, callback=None, saveFD=False)
stimulator.sham(t_sham_post, plasticity=True, clusterize_=True, saveFD=False)
