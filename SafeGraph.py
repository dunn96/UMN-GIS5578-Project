'''
Maisong Francis

This script reduces tabular monthly SafeGraph patterns to the seven metropolitan counties in 
Minnesota. The multiple SafeGraph files for each month are also reduced to schema of interest 
through index and combined into one file per month. This script also geocodes the points of 
interest within the seven metropolitan counties. 

This tool requires the arcpy module and the business analyst extension to use the ESRI USA geocoder.
'''

import gzip
from glob import glob
import pandas as pd
import arcpy 

# Directory of unzipped safegraph patterns csv.gz files
data_dir = r'C:\Users\msong\Desktop\2019_safegraph2'
#data_dir = r'F:\GIS Programming\2019_safegraph_all'
#data_dir = r'C:\Users\msong\Desktop\alldata'

def monthly(directory, month):
    '''combine all SafeGraph data for each month into one csv
    
    Parameters
    ----------
    directory: str
        Directory where csv files are
    month: str
        First three characters of month and last two digits of             year (i.e. jan20) for data to be combined
        
    output
    -------
    csv
        Combined data for each month
    '''
    
    df_list = []
    for file in glob(data_dir + r'\*.csv'):
        if f'{file[-23:-18]}' == month: # outputs monYY
            df = pd.read_csv(file)
            df_list.append(df)
        
    final_df = pd.concat(df_list)
    final_df.to_csv(f'{month}.csv', index=False)
    print(f'{month} data are combined')

##############################################################################   
# Columns to keep from each dataset
cols = ['safegraph_place_id', 
        'location_name', 
        'street_address', 
        'city', 
        'region',
        'postal_code',
        'brands',
        'date_range_start',
        'date_range_end',
        'raw_visit_counts',
        'raw_visitor_counts']

# Extract data for MN and output csv for each dataset. 
for file in glob(data_dir + r'\*.csv.gz'): # search folder for all csv.gz files
    with gzip.open(file, 'r') as data:
        df = pd.read_csv(data, 
                        usecols = cols)
 
        # Filter for MN data
        mn_df = df.loc[df['region'] == 'MN']

        # write to csv file
        outname = file
        mn_df.to_csv(f'{outname[:-7]}.csv', index=False)
        
##############################################################################
    
# Create list of all months in year

#data_dir = r'C:\Users\msong\Desktop\2019_safegraph2'
data_dir = r'F:\GIS Programming\2019_safegraph_all'
#data_dir = r'C:\Users\msong\Desktop\alldata'

months = []
for file in glob(data_dir + r'\*.csv'):
    months.append(file[-23:-18])
months = list(set(months)) # remove duplicates in list

# combine all monthly data for all months per year
for month in months:
    monthly(data_dir, month)

##############################################################################
    
# Reduce statewide safegraph data to seven county metropolitan area MN

#data_dir = r'C:\Users\msong\Desktop\2019_safegraph2'
#data_dir = r'F:\GIS Programming\2019_safegraph_all'
data_dir = r'C:\Users\msong\Desktop\alldata'

metro_dbf = r'C:\Users\msong\Desktop\shp_bdry_metro_counties_and_ctus\CountiesAndCTUs.dbf' 
out_path = r'C:\Users\msong\Desktop\metro'
paths = []

# Extract List of cities in seven metropolitan counties
cur = arcpy.da.SearchCursor(metro_dbf)
metro_cities = []
for row in cur:
    metro_cities.append(row.getValue('CTU_NAME'))
    
# Reduce monthly safegraph data to cities in the metro
for file in glob(data_dir + r"\*.csv"):
    with open(file) as data: 
        df = pd.read_csv(data)
        metro_df = df.loc[df['city'].isin(metro_cities)]
        metro_df.to_csv(f'{out_path}/{file[-9:-4]}_metro.csv', index=False)
                
##############################################################################        
        
# Geocode SafeGraph POI in metro. Outpoint point features .shp files for each month.
# Uses arcpy and Esri Business Anaylst US data geocoder
geocoder = r'\\files.umn.edu\us\gis\U-Spatial\UMN_Users\data\Esri Data\Esri BA USA 2019 geocoding data\USA.loc'
address_fields = ('Address street_address VISIBLE NONE;City city VISIBLE NONE;Region region VISIBLE NONE;Postal postal_code VISIBLE NONE')
out_path = r'C:\Users\leex6165\Desktop\geocoded'

# Get full path of each metro csv 
tables = glob(f'{out_path}\*.csv')
    
# Geocode safegraph poi into points based on multiple fields
# Output is in format: monYY_metro.shp i.e. jan19_metro.shp
for table in tables:
    arcpy.geocoding.GeocodeAddresses(table, 
                                     geocoder, 
                                     address_fields, 
                                     f'{out_path}\\{table[32:-4]}.shp', 
                                     "STATIC", 
                                     None, 
                                     '', 
                                     None)
    
