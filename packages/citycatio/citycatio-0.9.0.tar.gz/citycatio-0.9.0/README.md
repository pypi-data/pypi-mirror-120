# CityCAT I/O

[![test](https://github.com/nclwater/citycatio/workflows/build/badge.svg)](https://github.com/nclwater/citycatio/actions)

CityCAT I/O is a Python package that creates input files and reads output files.

## Tests

`python -m unittest`

## Dependencies

See environment.yml

## CLI Tools

### ccat2gtif
Usage: ccat2gtif [OPTIONS]

Options:  
  --in_path TEXT    Input path  
  --out_path TEXT   Output path  
  --srid TEXT       Coordinate reference system  
  --delimiter TEXT  Column delimiter of CSV file  
  --help            Show this message and exit.

Example:  
`ccat2gtif --in_path R1C1_SurfaceMaps/R1_C1_max_depth.csv --out_path max_depth.tif`

### geom2ccat
Usage: geom2ccat [OPTIONS]

Options:  
  --in_path TEXT   Input path  
  --out_path TEXT  Output path  
  --help           Show this message and exit.
  
 Example:  
`geom2ccat --in_path green_areas.shp --out_path GreenAreas.txt`
