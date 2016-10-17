# LibraryDataAnalysisScripts

This program can be used to generate graphs stored in GraphML format from csv/excel files that contain relatable data.

**Prerequisites**:
This program requires the following Python libraries to work properly.
- networkx
- matplotlib
- pandas

Recommended python version: > 3.4.3

You can install them using the following command.
```
pip install networkx matplotlib pandas
```

Basic usage:

For generating graph from csv files:
```
>>>python3 graphGen.py -h
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

For generating graph from excel files:
```
>>>python3 graphGenFromExcel.py -h
usage: graphGenFromExcel.py [-h] [-i [filename]] [-o [filename]] [--show] [--node [column number]]
                            [--relation [column number]]

Generate GraphML file from excel file.

optional arguments:
  -h, --help            show this help message and exit
  -i [filename]         input excel file name.
  -o [filename]         output file name for generated GraphML file.
  --show                Show generated graph using matplotlib.
  --node [column number]
                        Column number of data used to generate nodes.
  --relation [column number]
                        Column number of data used to build relations between nodes.
```