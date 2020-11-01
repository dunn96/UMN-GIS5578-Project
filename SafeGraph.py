import gzip
import glob
import csv
import geopandas as gpd
import pandas as pd

inFile = 'jan19patterns-part1.csv.gz'

# Obtain fieldnames from file
inFile = 'jan19patterns-part1.csv.gz'

with gzip.open(inFile, 'rt') as jan19:
    reader = pd.read_csv(jan19)
    
    # Extract list of column names and create new data frame with fields of interest
    all_col = []
    for col in reader.head():
        all_col.append(col)
    ex_col = all_col[:11] # fields of interest are first 12 fields
    df = reader.filter(ex_col)
 
# Filter for data in MN
mn_df = df.loc[df['region'] == 'MN']