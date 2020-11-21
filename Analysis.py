import geopandas as gpd

# Load in all the clipped shapefiles
water2014 = gpd.read_file("water2014_clip.shp")
water2016 = gpd.read_file("water2016_clip.shp")
water2018 = gpd.read_file("water2018_clip.shp")
water2020 = gpd.read_file("water2020_clip.shp")

# Get a user input for the size of the buffer
buffer_size = int(input("Provide a distance for the size of the buffer in meters: "))

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

# Calling the buffer_lakes function for each year of the impaired 
# water datasets and assigning them to new variables
buffer2014 = buffer_lakes(buffer_size, water2014)
buffer2016 = buffer_lakes(buffer_size, water2016)
buffer2018 = buffer_lakes(buffer_size, water2018)
buffer2020 = buffer_lakes(buffer_size, water2020)