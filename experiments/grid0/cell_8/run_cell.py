import os, sys, copy, warnings

sys.path.append('/home/roman/CODE/spiking-autoencoder')

from modules.utils import plotSTDP
from modules.cClasses_10b import cClassOne
from modules.utils import *
from modules.constants import bar_format, ROOT, COLORS

import matplotlib

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

# =======================

cell_id = int(sys.argv[1])

# read in the praram grid
grid = pd.read_csv('grid.csv')

astro = bool(grid.iloc[cell_id].astro)
stim_strength = float(grid.iloc[cell_id].stim_strength)
mex = float(grid.iloc[cell_id].mex)
use_thetas = bool(grid.iloc[cell_id].use_thetas)
HAGA = bool(grid.iloc[cell_id].HAGA)
symmetric = bool(grid.iloc[cell_id].symmetric)
patternLenMs = 10
nass = 20
t_sham_init = int(grid.iloc[cell_id].t_sham_init)
t_stim = int(grid.iloc[cell_id].t_stim)
t_sham = int(grid.iloc[cell_id].t_sham)

EXPERIMENT_HOME = f"{os.getcwd()}"  # no trailing slash
PATH2EXPDATA = 'data'
# =======================

# for fn in os.listdir(f"{EXPERIMENT_HOME}/{PATH2EXPDATA}"):
#     if not fn.startswith('res_'):
#         os.remove(f"{EXPERIMENT_HOME}/{PATH2EXPDATA}/{fn}")

params = load_config(f'{ROOT}/configs/config_sequential.yaml')
matplotlib.rcParams.update(load_config(f'{ROOT}/configs/rcparams.yaml'))

dt = params['dt']
NEo = params['NEo']
NM = params['NM']

# NE = 2000 #params['NE']
NE = params['NE']

# NI = 500 #params['NI']
NI = params['NI']

case = params['case']
wide = params['wide']

UU = simple_make_UU(NE, case, wide)
for k, v in {
        'HAGA': HAGA,
        'symmetric': symmetric,
        'U': np.mean(UU),
        'Cp': 0.14,
        'Cd': 0.0,
        'taustf': 350.0,
        'taustd': 250.0,
        'tpp': 15.1549,  #5.1549, #
        'tpd': 120.4221  #5.4221, #
}.items():
    params[k] = v

m = cClassOne(NE, NI, NEo, cell_id, home=f'{ROOT}/modules')
m.setParams(params)
m.saveSpikes(1)

m.set_useThetas(use_thetas)
cprint(f'use_thetas: {m.get_useThetas()}', color='magenta')

if astro:
    m.setUU(np.ascontiguousarray(UU))

stimulator = Stimulator(
    m,
    stim_strength=stim_strength,
    nass=nass,
    rotate_every_ms=patternLenMs,
    cell_id=cell_id,
    dump_stats=500,
)

m.set_mex(mex)

stimulator.sham(t_sham_init, plasticity=True, clusterize_=True)
stimulator.train(t_stim, patternLenMs=patternLenMs, clusterize_=True)
stimulator.sham(t_sham, plasticity=True, clusterize_=True)

# load data snapshots from the simulation you've just run

ref_t = t_sham_init + t_stim  # which time (ms) to use as a reference
# ref_t = t_stim # which time (ms) to use as a reference

snapl = SnapshotLoader(EXPERIMENT_HOME, PATH2EXPDATA, NE)
T, CORR, MOD = snapl.get(cell_id, ref_t=ref_t)

d = dict(
    t_sham_init=t_sham_init,
    t_stim=t_stim,
    t_sham=t_sham,
    HAGA=HAGA,
    astro=astro,
    symmetric=symmetric,
    T=T,
    MOD=MOD,
    cell_id=cell_id,
    mex=mex,
    stim_strength=stim_strength,
)

np.save(f"{EXPERIMENT_HOME}/{PATH2EXPDATA}/dump", d)
