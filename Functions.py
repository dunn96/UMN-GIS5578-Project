'''
Nicole Dunn and Maisong Francis

These are the functions to be used with the Analysis.py script. 
These functions buffers lake features based on user input and gets 
visitation counts within each lake buffer. The results are statistical 
outputs of visitation counts per month and year for each category of 
impairment status: impaired and nonimpaired, and prints top five most 
and least visited lakes for each year. The script also prints the removed 
and added lakes between each biennial impaired waters dataset. 
'''

import geopandas as gpd

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
    '''Prints most visited and least visted lakes with impairment status and 
    visitation counts. 
   
    Parameters
    ----------
    counts_df: gpd DataFrame
       The dataframe produced from spatial joining visitation counts to lake 
       buffers.
    year: str
       The year of the impaired waters dataset
       
    Prints
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
    ''' Prints removed and added impaired lakes between two biennial 
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
    
    Prints
    --------
    str
        The number of impaired lakes removed and added, and the names of those lakes. 
    '''
    
    added = y2_df.loc[y2_df['AUID'].isin(y1_df['AUID']) == False]
    removed = y1_df.loc[y1_df['AUID'].isin(y2_df['AUID']) == False]
    
    print(f"\nThere were {len(removed['NAME'])} lakes removed from impaired waters list {y1}-{y2}:")
    for row in removed['NAME']:
        print (row)
    
    print(f"\nThere were {len(added['NAME'])} lakes added to impaired waters list {y1}-{y2}:")
    for row in added['NAME']:
        print(row)             
        