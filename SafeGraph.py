import gzip
import glob
import pandas as pd

# Directory of unzipped safegraph csv.gz files
pathway = r'C:\Users\msong\Desktop\2019_safegraph2'

# Extract data for MN and output csv for each dataset. 
for file in glob.glob(pathway + "\*.csv.gz"):
    with gzip.open(file, 'r') as data:
        reader = pd.read_csv(data)
    
        # Extract list of column names and create new data frame with fields of interest
        all_col = []
        for col in reader.head():
            all_col.append(col)
        
        # fields of interest are first 12 fields for 2019, first 14 fields for 2020
        ex_col = all_col[:11] 
        df = reader.filter(ex_col)
 
        # Filter for MN data
        mn_df = df.loc[df['region'] == 'MN']

        # write to csv file
        outname = file
        mn_df.to_csv(f'{outname[:-7]}.csv', index=False)
        


def monthly(directory, month):
    """combine all data for each month into one csv
    
    Parameters
    ----------
    directory: str
        Directory of .csv files created from line 26
    month: str
        First three characters of month and last two digits of year (i.e. jan20) for data to be combined 
    """
    
    df_list = []
    for file in glob.glob(directory + "\*.csv"):
        if f'{file[-23:-18]}' == month:
            reader = pd.read_csv(file)
            df_list.append(reader)
        else:
            pass      
    final_df = pd.concat(df_list)
    final_df.to_csv(f'{month}.csv', index=False)
    print(f'{month} data are combined')
    

# Combine January 2020 data 
# [Having trouble turning looping through months in year2020
# and placing month parameter into monthly function]

directory = r'F:\GIS Programming\2019_safegraph_all'

# create list of all months in year
year2020 = []

for file in glob.glob(directory + "\*.csv"):
    year2020.append(file[-23:-18])

year2020 = list(set(year2020)) # remove duplicates in list


# combine all monthly data for all months per year
for month in year2020:
    month = month
    monthly(directory, month)
