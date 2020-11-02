import pandas as pd
import geopandas as gpd

water2018 = gpd.read_file("zip://impaired_2018_lakes.zip")

water2018.plot()
water2018.head()

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
water2018 = water2018.drop(["CAT", "CAT_DESC", "REACH_DESC", "AREA_ACRES", "AFFECTED_U", "LIKE_MEET", "NON_POLL", 
                            "NAT_BACK", "ADD_MON", "APPROVED", "NEEDS_PLN", "NEW_IMPAIR", "HUC_8", "HUC_8_NAME", 
                            "HUC_4", "BASIN", "COUNTY", "TRIBAL_INT", "INDIAN_RES", "AMMONIA", "CHLORIDE", 
                            "FISHESBIO", "HG_F", "HG_W", "NUTRIENTS", "PCB_F", "PFOS_F", "Shape_Leng", "Shape_Area"], axis = 1)

water2016 = water2016.drop(["CAT", "DATASET_NA", "REACH_DESC", "AREA_ACRES", "AFFECTED_U", "TMDL_NOT_R", "TMDL_NOT_1", 
                            "IMPAIR_P_1", "NEW_IMPAIR", "NEW_IMPA_1", "TMDL_APPRO", "TMDL_APP_1", "TMDL_NEEDE", "TMDL_NEE_1", 
                            "HUC_8", "HUC_8_NAME", "HUC_4", "BASIN", "COUNTY", "TRIBAL_INT", "INDIAN_RES", "CHLORIDE", 
                            "FISHESBIO", "HG_F", "HG_W", "NUTRIENTS", "PCB_F", "PFOS_F", "SHAPE_Leng", "SHAPE_Area"], axis = 1)

water2014 = water2014.drop(["LOCATION", "ACRES", "CAT", "AFFECTED_U", "NOPLN", "APPROVED", "NEEDSPLN", "NEW_2014", 
                            "HUC8", "HUC8_NAME", "HUC4", "BASIN", "ALL_COUNTI", "WDWMO_NAME", "WDWMO_TYPE", "Chloride", 
                            "HgF", "HgW", "Nutrients", "PCBF", "PFOS_W", "SHAPE_Leng", "Shape_Le_1", "Shape_Area"], axis = 1)

# Renaming the water_name column to match the two other datasets
water2018.rename(columns = {"IMP_PARAM" : "IMPAIR_PAR"})
water2014.rename(columns = {"WATER_NAME" : "NAME"})


# Loading the draft 2020 impaired water list
water2020 = gpd.read_file("wq-iw1-65.csv")

# retreiving all the column names
for col in water2020.columns:
    print(col)

# Sampling the data, to get a look at what we are dealing with
water2020.head()

# Selecting out the columns we want to keep
water2020 = water2020[["Water body name", "AUID", "Water body type", "Use Class", "Pollutant or stressor", "geometry"]]
water2020.head()

# Selecting out only the lake features to keep in line with the 3 other shapefiles we are already working with
water2020_lake = water2020.loc[(test["Water body type"] == "Lake")]

# Removing duplicate records --> grouping by AUID, and joining the polluatant or stressor field with ";" when they differ
# for the repeated AUID. This happens because a lake can have more than one stressor to get on the impaired water list.
water2020_remove_duplicates = water2020_lake.groupby("AUID", as_index = False)["Pollutant or stressor"].apply(";".join)
water2020_remove_duplicates

# Failed attempt to join the other needed columns back to the dataset after removing the duplicates
jointest1 = water2020_remove_duplicates.merge(water2020_lake, how = "inner", on = "AUID")
jointest1

# Attempt to get geometry for the 2020 dataset from the 2018 dataset
# Have not figured out the best way to do this yet. 
jointest2 = water2020_remove_duplicates.merge(water2018, on = "AUID")
jointest2


# Loading block group data
blockgroups_df = gpd.read_file('zip://tl_2019_27_bg.zip')
print(f'Loaded {len(blockgroups_df):,} block groups')

# Checking the projections of the blockgroups and the water layers
print(blockgroups_df.crs)
print(water2018.crs)

# Reprojecting the blockgroups to match the water
bg_proj = blockgroups_df.to_crs('EPSG:26915')
bg_proj.plot()

# Intersecting the water 2018 layer with the blockgroups to have the blockgroup ids for each lake.
water2018_intersect_bg_proj = gpd.overlay(water2018, bg_proj, how='intersection')
water2018_intersect_bg_proj.plot()
water2018_intersect_bg_proj.head()