import gzip
import glob
import csv
import geopandas as gpd
import pandas as pd

# Directory of unzipped safegraph csv.gz files
pathway = r'C:\Users\msong\Desktop\2019_safegraph2'

for file in glob.glob(pathway + "\*.csv.gz"):
    with gzip.open(file, 'r') as data:
        reader = pd.read_csv(data)
    
        # Extract list of column names and create new data frame with fields of interest
        all_col = []
        for col in reader.head():
            all_col.append(col)
        ex_col = all_col[:11] # fields of interest are first 12 fields
        df = reader.filter(ex_col)
 
        # Filter for MN data
        mn_df = df.loc[df['region'] == 'MN']

        # write to csv file
        outname = file
        mn_df.to_csv(f'{outname[:-7]}.csv', index=False)
    