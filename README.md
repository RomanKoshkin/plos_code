# Code for "Astrocyte Regulation of Synaptic Plasticity Balances Robustness and Flexibility of Cell Assemblies"

This repo contains essential code for reproducing the results reported in the paper "Astrocyte Regulation of Synaptic Plasticity Balances Robustness and Flexibility of Cell Assemblies".

## Preliminaries

#### 1 Clone the repo

git clone git@github.com:RomanKoshkin/plos_code.git

#### 2 Install the dependencies into a clean enviroment

```bash
uv venv .venv --python=3.8.13 && source .venv/bin/activate && uv pip install -r requirements.txt
```

#### 3 Build the model's c++ core for you system

```bash
bash scripts/build_pybind.sh noopenmp
```

## Quickstart

To run one experiment (e.g. from Fig.6):

```bash
cd experiments
python run_cell_Fig6.py 0  # where 0 is the row id in `grid_Fig6.csv` (the grid of model parameters).
```

All the experiments were run using the codebase in this repo with difference parameters. You can run an experiment similar to Fig. 6, but also cofigure your own model (size, STP, STDP and connectivity parameters) as well as simulation regime (frequency, etc.)

The model will be saving data dumps to `experiments/Fig6` which you can use to plot figures to understand the behavior of the model. 
