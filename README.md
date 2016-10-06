# LibraryDataAnalysisScripts

This program can be used to generate graphs stored in GraphML format from csv files that contain relatable data.

**Prerequisites**:
This program requires the following Python libraries to work properly.
- networkx
- matplotlib
You can install them using the following command.
```
pip install networkx matplotlib
```

Basic usage:
```
>>>python graphGen.py -h
usage: graphGen.py [-h] [-i [filename]] [-o [filename]] [--show]
                   [--node [column number]] [--relation [column number]]

Generate GraphML file from csv file.

optional arguments:
  -h, --help            show this help message and exit
  -i [filename]         input csv file name.
  -o [filename]         output file name for generated GraphML file.
  --show                Show generated graph using matplotlib.
  --node [column number]
                        Column number of data used to generate nodes.
  --relation [column number]
                        Column number of data used to build relations between
                        nodes.
```