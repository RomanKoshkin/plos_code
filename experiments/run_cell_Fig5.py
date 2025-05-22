# NOTE: make sure to use `engine='python'` if you use `pandas.read_csv`
#
import numpy as np  # import pandas as pd

np.random.seed(42)
import os, sys, warnings
from pprint import pprint

sys.path.append('../')
print(f'PID: {os.getpid()}')

from modules_pybind.python_wrapper import Model  # here will wrap the c++ object with Python

from modules.utils import *
from modules.constants import ROOT

warnings.filterwarnings("ignore")

# --------------------------------------------------------------------------------------------------

grid = pd.read_csv('grid_Fig5.csv', engine='python')

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
t_sham = int(grid.iloc[cell_id].t_sham)  #True

# --------------------------------------------------------------------------------------------------

params = load_config(f'{ROOT}/configs/config_sequential.yaml')

dt = params['dt']
NEo = params['NEo']
NM = params['NM']

NE = params['NE']
NI = params['NI']
N = NE + NI

case = params['case']
wide = params['wide']

UU = simple_make_UU(NE, case, wide)

for k, v in {
        'HAGA': HAGA,
        'symmetric': symmetric,
        'U': np.mean(UU),
        'Cp': Cp,  # NOTE: !!!! was 0.14
        'Cd': Cd,  # NOTE:!!!!
        'taustf': taustf,
        'taustd': taustd,
        'tpp': 15.1549,  #5.1549, #
        'tpd': 120.4221  #5.4221, #
}.items():
    params[k] = v

m = Model(NE, NI, NEo, cell_id)
m.setParams(params)
m.saveSpikes(True)

m.m.soft_clip_dw = False
cprint(f'Using soft_clip_dw: {m.m.soft_clip_dw}', color='red', attrs=['bold'])
time.sleep(2)

# UU = np.random.choice(UU, size=N)
if astro:
    UU[NE:] = 1.0
else:
    UU[:NE] = np.mean(UU)
    UU[NE:] = 1.0
m.setUU(UU)

m.set_useThetas(False)
m.get_useThetas()

patternLenMs = 20
nass = 20

# NOTE: change E->E weights
# w = m.getWeights()
# for i in range(NE):
#     for j in range(NE):
#         if w[i, j] > 0.001:
#             w[i, j] = 0.15 * (4.0 + 0.8 * np.random.randn())
# m.setWeights(w)

# m.set_Jmax(9.0)  # NOTE: prohibit clipping

m.set_mex(0.3)

m.m.stp_on_I = False  # NOTE: False by default FIXME: change stpOnSpike for inhibitory neurons (make it slower)
m.m.dump_dw = True
datafolder = "data_Fig5"
m.m.datafolder = datafolder

# NOTE: frezing all wts except EE
frozens = m.getFrozens()
frozens[:, NE:] = True
frozens[NE:, :] = True
m.setFrozens(frozens)

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
stimulator.sham(t_sham, plasticity=True, clusterize_=True, saveFD=False)