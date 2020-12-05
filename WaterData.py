'''
This python script's purpose is to clean spatial data files that will be used in 
future analysis. Cleaning the data includes clipping all the data to the 7 county metro as the area of interest, 
removing fields that are not needed, removing invalid geometries from the geodataframes, 
and adding geometery where there is none.
'''

import pandas as pd
import geopandas as gpd

# Loading all shapefile datasets in as geopandas dataframes and assiging to variables
hydrography = gpd.read_file("zip://shp_water_dnr_hydrography.zip")
water2018 = gpd.read_file("zip://impaired_2018_lakes.zip")
water2016 = gpd.read_file("zip://impaired_2016_lakes.zip")
water2014 = gpd.read_file("zip://impaired_2014_lakes.zip")
metro = gpd.read_file("zip://shp_bdry_metro_counties_and_ctus.zip")

##############################################################################

### CLEANING AND CLIPPING IMPAIRED WATER 2014, 2016, AND 2018

## Dropping all the unnecessary columns
water2018 = water2018.drop(["CAT", "CAT_DESC", "REACH_DESC", "USE_CLASS", "AFFECTED_U", "LIKE_MEET", 
                            "NON_POLL", "NAT_BACK", "ADD_MON", "APPROVED", "NEEDS_PLN", "IMP_PARAM", 
                            "NEW_IMPAIR", "HUC_8", "HUC_8_NAME", "HUC_4", "BASIN", "TRIBAL_INT", 
                            "INDIAN_RES", "AMMONIA", "CHLORIDE", "FISHESBIO", "HG_F", "HG_W", "NUTRIENTS", 
                            "PCB_F", "PFOS_F", "Shape_Leng", "Shape_Area"], axis = 1)

water2016 = water2016.drop(["CAT", "DATASET_NA", "REACH_DESC", "USE_CLASS", "AFFECTED_U", "TMDL_NOT_R", 
                            "TMDL_NOT_1", "IMPAIR_PAR", "IMPAIR_P_1", "NEW_IMPAIR", "NEW_IMPA_1", 
                            "TMDL_APPRO", "TMDL_APP_1", "TMDL_NEEDE", "TMDL_NEE_1", "HUC_8", "HUC_8_NAME", 
                            "HUC_4", "BASIN", "TRIBAL_INT", "INDIAN_RES", "CHLORIDE", "FISHESBIO", "HG_F", 
                            "HG_W", "NUTRIENTS", "PCB_F", "PFOS_F", "SHAPE_Leng", "SHAPE_Area"], axis = 1)

water2014 = water2014.drop(["LOCATION", "CAT", "AFFECTED_U", "NOPLN", "APPROVED", "NEEDSPLN", "IMPAIR_PAR", 
                            "NEW_2014", "HUC8", "HUC8_NAME", "HUC4", "BASIN", "WDWMO_NAME", "WDWMO_TYPE", 
                            "Chloride", "HgF", "HgW", "Nutrients", "PCBF", "PFOS_W", "SHAPE_Leng", 
                            "Shape_Le_1", "Shape_Area"], axis = 1)

# Renaming the columns in 2014 to match the two other years
water2014 = water2014.rename(columns = {"WATER_NAME" : "NAME", "ALL_COUNTI" : "COUNTY", "ACRES" : "AREA_ACRES"})

## Preping each dataframe for clippling
# Locate all invalid gometries and drop them from the dataset
water2018_drop_invalid = water2018.loc[water2018['geometry'].is_valid, :]

water2016_drop_invalid = water2016.loc[water2016['geometry'].is_valid, :]

water2014_drop_invalid = water2014.loc[water2014['geometry'].is_valid, :]

# Cleaning the metro dataset, dissolving on the county name
metro_dissolve = metro.dissolve(by = "CO_NAME")

# Clipping the three impaired water files to the 7 county metro
water2018_clip = gpd.clip(water2018_drop_invalid, metro_dissolve)
water2016_clip = gpd.clip(water2016_drop_invalid, metro_dissolve)

# 2014 needed to be reprojected - then clip was performed
water2014_proj = water2014_drop_invalid.to_crs('EPSG:26915')
water2014_clip = gpd.clip(water2014_proj, metro_dissolve)

##############################################################################

### CLEANING THE 2020 IMPAIRED WATER DATA SET

# Load water 2020 data csv, selecting out the columns that we want, adding a 
# geometry column, and pulling out only the lake features.
water2020 = gpd.read_file("wq-iw1-65.csv")
water2020 = water2020[["Water body name", "AUID", "County", "Water body type", "geometry"]]
water2020_lake = water2020.loc[(water2020["Water body type"] == "Lake")]

# Dropping the "water body type" field since it is no longer needed
water2020_lake = water2020_lake[["AUID", "Water body name", "County", "geometry"]]

# Renaming the columns to match the other years of impaired water data
water2020_lake = water2020_lake.rename(columns = {"Water body name" : "NAME", "County" : "COUNTY"})

# Selecting out the 7 county metro
counties = ["Anoka", "Hennepin", "Ramsey", "Washington", "Carver", "Scott", "Dakota"]
water2020_metro = water2020_lake.loc[(water2020_lake["COUNTY"].isin(counties))]

# Varifying all the correct counties are there
water2020_metro["COUNTY"].unique()

# Drop Duplicate AUIDs
water2020_clean = water2020_metro.drop_duplicates(subset = ["AUID"])

##############################################################################

### FINDING THE SMALLEST LAKE FEATURE WITHIN THE IMPAIRED WATER DATAFRAMES

# Creating a list of the gpdf 
dfs = [water2014_clip, water2016_clip, water2018_clip]
dfs_names = ["water2014_clip", "water2016_clip", "water2018_clip"]

# New field for impairment status in all data sets
for df in dfs:
    df["status"] = "Impaired"

def find_min(dfs):
    '''Finds the smallest lake within the impaired datasets
    
    Parameter
    ---------
    dfs : list
        The dataframes of impaired water features
    '''
    global minimum
    minimum = []
    for df in dfs:
        minimum.append(df["AREA_ACRES"].min())
    minimum = min(minimum)

# Find smallest lake size of from all impaired lakes
find_min(dfs)

##############################################################################

### CLEANING THE HYDROGRAPHY DATA SET

# Locate all invalid gometries and drop them from the dataset
hydro_drop_invalid = hydrography.loc[hydrography['geometry'].is_valid, :]

# Clipping hydro to the 7 county metro
hydro_clip = gpd.clip(hydro_drop_invalid, metro_dissolve)

# Narrowing down the number of features in the hydro layer to only lakes and ponds
hydro_lake = hydro_clip.loc[hydro_clip["wb_class"] == "Lake or Pond"]

# Selecting only the lakes that are at least the size of the the impaired water dataframes
hydro_lake = hydro_lake.loc[(hydro_lake["acres"] >= minimum)]

# Dropping all excess fields from the dataframe
hydro_clean = hydro_lake.drop(["fw_id", "dowlknum", "sub_flag", "wb_class", "lake_class", 
                               "shore_mi", "center_utm", "center_u_1", "dnr_region", "fsh_office", 
                               "outside_mn", "delineated", "delineatio", "delineat_1", "delineat_2", 
                               "approved_b", "approval_d", "approval_n", "has_flag", "flag_type", 
                               "publish_da", "lksdb_basi", "has_wld_fl", "wld_flag_t", "created_us", 
                               "created_da", "last_edite", "last_edi_1", "ow_use", "pwi_class", "map_displa", 
                               "shape_Leng", "shape_Area", "INSIDE_X", "INSIDE_Y", "in_lakefin"], axis = 1)

# New field for impairment status to be used when data is joined with the imparied data sets
hydro_clean["status"] = ""

# Dissolve hydrography geometry by lake name 
hydro_clean = hydro_clean.rename(columns={'pw_basin_n': 'NAME'})
hydro_dis = (hydro_clean.dissolve(by='NAME')).reset_index()

##############################################################################

### JOINING DNR CLEAN HYDRO DATAFRAME TO THE IMPAIRED WATER DATAFRAMES

def complete_hydro(waterdata, waterdata_name):
    '''Joins the cleaned hydrography dataframe to the 
    impaired water dataframes to create complete
    dataframes of impaired/non-impaired features.
    
    Parameters
    ----------
    waterdata : list
        A list of the dataframes of impaired water features
    waterdata_name: list
        A list of names for the impaired water files
    '''
    # Combine nonimpaired with impaired. Returns a pandas dataframe
    join_hydro = hydro_dis.merge(waterdata, on ='NAME', how='left') 
    
    # Set geometry to hydro_dis dataset for all features
    projected = join_hydro.set_geometry(join_hydro['geometry_x'], 
                                        crs='EPSG:26915')
    
    # Combine duplicate features
    projected_dis = (projected.dissolve(by='NAME')).reset_index() 
    
    # Pulling out the fields to keep
    projected_dis = projected_dis[['NAME', 
                                   'geometry', 
                                   'acres', 
                                   'cty_name', 
                                   'unique_id', 
                                   'status_y']]
    
    # Fill status of nonimpaired lakes
    projected_dis = projected_dis.fillna("nonimpaired")
    projected_df = projected_dis.rename(columns = {'status_y': 'status'})

    projected_df.to_file(f'{waterdata_name}.shp')

# Nonimpaired and impaired completed dataset for each year    
for df in dfs:
    for name in dfs_names:
        complete_hydro(df, name)

    
##############################################################################

### JOINING GEOMETRY TO WATER2020_CLEAN

water2020_join_auid = water2020_clean.merge(water2018_clip, how = "left", on = "AUID")

water2020_join_auid = water2020_join_auid[["AUID", "NAME_x", "COUNTY_x", "AREA_ACRES", "geometry_y", "status"]]

water2020_join_auid = water2020_join_auid.rename(columns = {"NAME_x" : "NAME", "COUNTY_x" : "COUNTY", "geometry_y" : "geometry"})

complete_hydro(water2020_join_auid, "water2020_clip")
