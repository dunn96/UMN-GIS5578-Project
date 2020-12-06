'''
Nicole Dunn and Maisong Francis

This script is designed to be used after WaterData.py and SafeGraph.py.
This script buffers lake features based on user input and gets visitation counts
within each lake buffer. The results are statistical outputs of visitation 
counts per month and year for each category of impairment status: impaired and 
nonimpaired, and returns top five most and least visited lakes for each year. 
'''

import geopandas as gpd

# Load in all the clipped shapefiles
water2014 = gpd.read_file("water2014_clip.shp")
water2016 = gpd.read_file("water2016_clip.shp")
water2018 = gpd.read_file("water2018_clip.shp")
water2020 = gpd.read_file("water2020_clip.shp")


def buffer_lakes(buffer, water_feat):
    ''' Buffer the clipped impaired water features.
    Parameters:
    -----------
    buffer: int
        The user obtained distance for the buffer function
    water_feat: geodataframe
        The geodataframe of an impaired water dataset
    
    Return:
    -------
    lake_buffer: geodataframe
        The buffer around each lake feature in the impaired water dataframe
    '''
    lake_buffer = gpd.GeoDataFrame(water_feat.buffer(buffer))
    lake_buffer["NAME"] = water_feat["NAME"]
    lake_buffer = lake_buffer.set_geometry(lake_buffer[0])
    lake_buffer = lake_buffer[["NAME", "geometry"]]
    return lake_buffer


# Counts of visitation for nonimpaired and impaired lakes 2020
def vis_stats(counts_df):
    '''
    add documentation
    '''
    vis = counts_df.groupby(['STATUS']).sum()
    lkcounts = counts_df.groupby(['STATUS'])['NAME'].count()

    vis['avg monthly vis'] = vis.mean(axis=1)
    vis['Lake Counts'] = lkcounts
    vis['Total visits'] = (vis.sum(axis=1))
    vis['Total visits'] = vis['Total visits'] - (vis['avg monthly vis'] + vis['Lake Counts'])
    vis['Avg monthly vis per lake'] = vis['avg monthly vis'] / vis['Lake Counts']
    vis['Avg yearly vis per lake'] = vis['Total visits'] / vis['Lake Counts']
    vis.loc['Total vis per month']= vis.sum(axis=0)
    return vis


def min_max(counts_df, year):
   '''
   add documentation
   '''
    total = counts_df
    total['Total visits'] = total.sum(axis=1)

    maximum = total.sort_values(by=['Total visits'], 
                                ascending=False, 
                                ignore_index=True)
    print(f'The top five most visted lakes for {year} are: ')
    for row in range(len(maximum[0:5])):
        print(f"Lake Name: {maximum['NAME'][row]}"
              f"\nTotal visits: {maximum['Total visits'][row]}"
              f"\nStatus: {maximum['STATUS'][row]}\n")

    minimum = total.sort_values(by=['Total visits'], 
                                ascending=True, 
                                ignore_index=True)
    
    print(f'The top five least visted lakes for {year} are: ')
    for row in range(len(minimum[0:5])):
        print(f"Lake Name: {minimum['NAME'][row]}"
              f"\nTotal visits: {minimum['Total visits'][row]}"
              f"\nStatus: {minimum['STATUS'][row]}\n")
   
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
directory = r'/home/leex6165/gisproj/'
path = f'{directory}*19_metro.zip'

buffer = buffer2018
data_2018 = pd.DataFrame({'NAME': buffer['NAME'], 'STATUS': water2018['status']})

# Get counts in each lake buffer per month for 2018 water data and 2019 foot traffic
for file in glob.glob(path):
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

for file in glob.glob(path):
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
