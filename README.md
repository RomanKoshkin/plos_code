# Code for "Astrocyte Regulation of Synaptic Plasticity Balances Robustness and Flexibility of Cell Assemblies"

This repo contains essential code for reproducing the results reported in the paper "Astrocyte Regulation of Synaptic Plasticity Balances Robustness and Flexibility of Cell Assemblies".

## Preliminaries

#### 1 Clone the repo

git clone ...

#### 2 Install the dependencies into a clean enviroment

```bash
bash scripts/build_pybind.sh noopenmp
```

#### 3 Build the c++ core for you system


## Quickstart

All the experiments were run using the codebase in this repo with difference parameters. You can run an experiment similar to Fig. 6, but also cofigure your own model (size, STP, STDP and connectivity parameters) as well as simulation regime (frequency, etc.)

The model will be saving data dumps to `experiments/Fig6` which you can use to plot figures to understand the behavior of the model. 
