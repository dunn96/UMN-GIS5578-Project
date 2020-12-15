'''
Nicole Dunn and Maisong Francis

This script is designed to be used after WaterData.py and SafeGraph.py.
This script buffers lake features based on user input and gets visitation counts
within each lake buffer. The results are statistical outputs of visitation 
counts per month and year for each category of impairment status: impaired and 
nonimpaired, and prints top five most and least visited lakes for each year. 
The script also prints the removed and added lakes between each biennial 
impaired waters dataset. 
'''

import pandas as pd 
import geopandas as gpd
from glob import glob
from Functions import *

directory = r'/home/leex6165/gisproj/'

# Load in all the clipped shapefiles
water2014 = gpd.read_file("water2014_clip.shp")
water2016 = gpd.read_file("water2016_clip.shp")
water2018 = gpd.read_file("water2018_clip.shp")
water2020 = gpd.read_file("water2020_clip.shp")

# Load in impaired only clipped files
impaired2014 = gpd.read_file("water2014_impaired.shp")
impaired2016 = gpd.read_file("water2016_impaired.shp")
impaired2018 = gpd.read_file("water2018_impaired.shp")
impaired2020 = pd.read_csv("water2020_impaired.csv")

##############################################################################

# Get a user input for the size of the buffer
buffer_size = int(input("Provide a distance for the size of the buffer in meters: "))
              
# Calling the buffer_lakes function for each year of the impaired 
# water datasets and assigning them to new variables
buffer2014 = buffer_lakes(buffer_size, water2014)
buffer2016 = buffer_lakes(buffer_size, water2016)
buffer2018 = buffer_lakes(buffer_size, water2018)
buffer2020 = buffer_lakes(buffer_size, water2020)


##############################################################################

# Get all metro data by finding all files ending in _metro.zip
path = f'{directory}*19_metro.zip'

buffer = buffer2018
data_2018 = pd.DataFrame({'NAME': buffer['NAME'], 'STATUS': water2018['status']})

# Get counts in each lake buffer per month for 2018 water data and 2019 foot traffic
for file in glob(path):
    sg_data = f'zip://{file}'
    patterns = (gpd.read_file(sg_data)).to_crs('EPSG:26915')
    data_join = gpd.sjoin(buffer, patterns, op='intersects')

    # Get counts of points in each lake buffer.
    data_grp = data_join.groupby('NAME', as_index=False)['index_right'].count()
    data_grp = data_grp.rename(columns = {'index_right': f'{file[-15:-10]}_counts'})
    
    data_2018 = data_2018.merge(data_grp, how='outer')
    
    
##############################################################################    
    
# Get counts in each lake buffer per month for 2018 water data and 2019 foot traffic
path = f'{directory}*20_metro.zip'
buffer = buffer2020
data_2020 = pd.DataFrame({'NAME': buffer['NAME'], 
                          'STATUS': water2020['status']} )

for file in glob(path):
    sg_data = f'zip://{file}'
    patterns = (gpd.read_file(sg_data)).to_crs('EPSG:26915')
    data_join = gpd.sjoin(buffer, patterns, op='intersects')

    # Get counts of points in each lake buffer.
    data_grp = data_join.groupby('NAME', as_index=False)['index_right'].count()
    data_grp = data_grp.rename(columns = {'index_right': f'{file[-15:-10]}_counts'})
    
    data_2020 = data_2020.merge(data_grp, how='outer')
    
############################################################################## 

# Counts of visitation for nonimpaired and impaired lakes for each year
# Write results to csv
vis_2018 = vis_stats(data_2018)
vis_2018.to_csv(f'{directory}/vis_stats2018_{buffer_size}m.csv', 
                index=True)

vis_2020 = vis_stats(data_2020)
vis_2020.to_csv(f'{directory}/vis_stats2020_{buffer_size}m.csv', 
                index=True)


# Find most and least visited lake for each year
min_max(data_2018, "2018")
min_max(data_2020, "2020")

##############################################################################

# Finding added and removed lakes between each impaired dataset year
impaired_change(impaired2014, '2014', impaired2016, '2016')
impaired_change(impaired2016, '2016', impaired2018, '2018')
impaired_change(impaired2018, '2018', impaired2020, '2020')    
    
    
