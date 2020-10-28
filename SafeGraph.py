import gzip
import glob
import csv
import geopandas as gpd


inFile = 'jan19patterns-part1.csv.gz'

# open gz file and obtain field names
with gzip.open(inFile, 'rt') as jan19:
    reader = csv.DictReader(jan19)
    fields = []
    fields.append(reader.fieldnames)