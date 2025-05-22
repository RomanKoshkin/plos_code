ls | grep cell_ | xargs rm -r
python make_grid.py
python copy_files.py
python dispatcher.py 