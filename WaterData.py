'''
Author: Nicole Dunn

This python script purpose is to clean spatial data files that will be used in 
future analysis. Cleaning the data includes removing fields that are not needed, 
removing invalid geometries from the geodataframes, adding geometery where there 
is none, and clipping all the data to the 7 county metro as the area of interest.
'''

import pandas as pd
import geopandas as gpd

# Loading all shapefile datasets in as geopandas dataframes
hydrography = gpd.read_file("zip://shp_water_dnr_hydrography.zip")
water2018 = gpd.read_file("zip://impaired_2018_lakes.zip")
water2016 = gpd.read_file("zip://impaired_2016_lakes.zip")
water2014 = gpd.read_file("zip://impaired_2014_lakes.zip")
metro = gpd.read_file("zip://shp_bdry_metro_counties_and_ctus.zip")


# Cleaning the metro dataset, dissolving on the county name. 
metro_dissolve = metro.dissolve(by = "CO_NAME")

# There are many columns in this dataset,
# this is to be able to see all of them to easily
# choose the ones we will keep
for col in water2018.columns:
    print(col)
    
for col in water2016.columns:
    print(col)
    
for col in water2014.columns:
    print(col)

# Dropping all the unnecessary columns
water2018 = water2018.drop(["CAT", "CAT_DESC", "REACH_DESC", "USE_CLASS", "AREA_ACRES", "AFFECTED_U", "LIKE_MEET", 
                            "NON_POLL", "NAT_BACK", "ADD_MON", "APPROVED", "NEEDS_PLN", "IMP_PARAM", "NEW_IMPAIR", 
                            "HUC_8", "HUC_8_NAME", "HUC_4", "BASIN", "TRIBAL_INT", "INDIAN_RES", "AMMONIA", "CHLORIDE", 
                            "FISHESBIO", "HG_F", "HG_W", "NUTRIENTS", "PCB_F", "PFOS_F", "Shape_Leng", "Shape_Area"], axis = 1)

water2016 = water2016.drop(["CAT", "DATASET_NA", "REACH_DESC", "USE_CLASS", "AREA_ACRES", "AFFECTED_U", "TMDL_NOT_R", 
                            "TMDL_NOT_1", "IMPAIR_PAR", "IMPAIR_P_1", "NEW_IMPAIR", "NEW_IMPA_1", "TMDL_APPRO", "TMDL_APP_1", 
                            "TMDL_NEEDE", "TMDL_NEE_1", "HUC_8", "HUC_8_NAME", "HUC_4", "BASIN", "TRIBAL_INT", "INDIAN_RES", 
                            "CHLORIDE", "FISHESBIO", "HG_F", "HG_W", "NUTRIENTS", "PCB_F", "PFOS_F", "SHAPE_Leng", "SHAPE_Area"], axis = 1)

water2014 = water2014.drop(["LOCATION", "ACRES", "CAT", "AFFECTED_U", "NOPLN", "APPROVED", "NEEDSPLN", "IMPAIR_PAR", 
                            "NEW_2014", "HUC8", "HUC8_NAME", "HUC4", "BASIN", "WDWMO_NAME", "WDWMO_TYPE", "Chloride", 
                            "HgF", "HgW", "Nutrients", "PCBF", "PFOS_W", "SHAPE_Leng", "Shape_Le_1", "Shape_Area"], axis = 1)

# Renaming the columns to match the two other datasets
water2014 = water2014.rename(columns = {"WATER_NAME" : "NAME", "ALL_COUNTI" : "COUNTY"})


# Checking for valid geometries in the files in order to perform a clip operation
for i in water2018.is_valid:
    if i == False:
        print("poly is false")

# Locate all invalid gometries and drop them from the dataset
water2018_drop_invalid = water2018.loc[water2018['geometry'].is_valid, :]

# Checking for valid geometries in the files in order to perform a clip operation
for i in water2016.is_valid:
    if i == False:
        print("poly is false")

# Locate all invalid gometries and drop them from the dataset
water2016_drop_invalid = water2016.loc[water2016['geometry'].is_valid, :]

# Checking for valid geometries in the files in order to perform a clip operation
for i in water2014.is_valid:
    if i == False:
        print("poly is false")

# Locate all invalid gometries and drop them from the dataset
water2014_drop_invalid = water2014.loc[water2014['geometry'].is_valid, :]


# Clipping the three impaired water files to the 7 county metro
water2018_clip = gpd.clip(water2018_drop_invalid, metro_dissolve)
water2016_clip = gpd.clip(water2016_drop_invalid, metro_dissolve)

# 2014 needed to be reprojected - then clip was performed
water2014_proj = water2014_drop_invalid.to_crs('EPSG:26915')
water2014_clip = gpd.clip(water2014_proj, metro_dissolve)


# Checking for valid geometries in the files in order to perform a clip operation
for i in hydrography.is_valid:
    if i == False:
        print("poly is false")
        
# Locate all invalid gometries and drop them from the dataset
hydro_drop_invalid = hydrography.loc[hydrography['geometry'].is_valid, :]

# Clipping hydro to the 7 county metro
hydro_clip = gpd.clip(hydro_drop_invalid, metro_dissolve)

# Narrowing down the number of features in the hydro layer to only lakes and ponds
hydro_lake = hydro_clip.loc[hydro_clip["wb_class"] == "Lake or Pond"]





# Load water 2020 data csv, selecting out the columns that we want and addinga geometry column
# and pulling out only the lake features.
water2020 = gpd.read_file("wq-iw1-65.csv")
water2020 = water2020[["Water body name", "AUID", "Water body type", "geometry"]]
water2020_lake = water2020.loc[(water2020["Water body type"] == "Lake")]

# Dropping the "water body type" field since it is no longer needed
water2020_lake = water2020_lake[["Water body name", "AUID", "geometry"]]

# Renaming the columns to match the two other datasets
water2020_lake = water2020_lake.rename(columns = {"Water body name" : "NAME"})