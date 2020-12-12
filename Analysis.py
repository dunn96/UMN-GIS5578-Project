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

# Load in impaired only clipped files
impaired2014 = gpd.read_file("water2014_impaired.shp")
impaired2016 = gpd.read_file("water2016_impaired.shp")
impaired2018 = gpd.read_file("water2018_impaired.shp")
impaired2020 = pd.read_csv("water2020_impaired.csv")

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


def vis_stats(counts_df):
    ''' Compute statistical metrics for visitations to impaired and nonimpaired 
    lakes. Metrics include average month visits, lake counts, total visits, 
    averae month visits per lake, average yearly visits per lake, and total visits
    per year. 
    
    Parameter
    ----------
    counts_df: gpd DataFrame
        The dataframe produced from spatial joining visitation counts to lake 
        buffers.
        
    Return
    ------
    vis
        gpd dataframe with statistical metrics
    '''
    
    vis = counts_df.groupby(['STATUS']).sum()
    lkcounts = counts_df.groupby(['STATUS'])['NAME'].count()

    vis['avg monthly vis'] = vis.mean(axis=1)
    vis['Lake Counts'] = lkcounts
    vis['Total visits'] = (vis.sum(axis=1))
    vis['Total visits'] = vis['Total visits'] - (vis['avg monthly vis'] + vis['Lake Counts'])
    vis['Avg monthly vis per lake'] = vis['avg monthly vis'] / vis['Lake Counts']
    vis['Avg yearly vis per lake'] = vis['Total visits'] / vis['Lake Counts']
    vis.loc['Total vis per year']= vis.sum(axis=0)
    return vis


def min_max(counts_df, year):
   ''' Returns most visited and least visted lakes with impairment status and 
   visitation counts. 
   
   Parameters
   ----------
   counts_df: gpd DataFrame
       The dataframe produced from spatial joining visitation counts to lake 
       buffers.
   year: str
       The year of the impaired waters dataset
       
   Returns
   -------
   str
       Printed names, impairment status, and visitation counts of top five most
       and least visited lakes.
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

    
def impaired_change(y1_df, y1, y2_df, y2):
    ''' Returns removed and added impaired lakes between two biennial 
    impaired waters lists. 
    
    Parameters
    ----------
    y1_df: gpd DataFrame
        The impaired waters clipped to study area and written out from 
        WaterData.py and read with Geopandas.Must be the earlier year between 
        two dataframes being compared. 
    y1: str
        Year of earlier dataset
    y2_df:
        The impaired waters clipped to study area and written out from 
        WaterData.py and read with Geopandas. Must be the later year between 
        two dataframes being compared. 
    y2: str
        Year of the later dataset
    
    Returns:
    --------
    str
        The number of impaired lakes removed and added, and the names of those lakes. 
    '''
    
    added = y2_df.loc[y2_df['AUID'].isin(y1_df['AUID']) == False]
    removed = y1_df.loc[y1_df['AUID'].isin(y2_df['AUID']) == False]
    
    print(f"There were {len(removed['NAME'])} lakes removed from impaired waters list {y1}-{y2}:")
    for row in removed['NAME']:
        print (row)
    
    print(f"\nThere were {len(added['NAME'])} lakes added to impaired waters list {y1}-{y2}:")
    for row in added['NAME']:
        print(row)             
        
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

##############################################################################

### FINDING ADDED AND REMOVED LAKES BETWEEN EACH YEAR

impaired_change(impaired2014, '2014', impaired2016, '2016')
impaired_change(impaired2016, '2016', impaired2018, '2018')
impaired_change(impaired2018, '2018', impaired2020, '2020')    
    
    