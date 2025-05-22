# What it does

Runs a good grid of - astrocytes vs. no astrocytes.

# If you are lazy

`sh RUN_EVERYTHING.sh`

# How it does it

- `python make_grid.py` # defines and saves the grid
- `python copy_files.py` # creates folders and copies the necessary files to cell folders
- `python dispatcher.py` # runs all the grid cells simulaneously
