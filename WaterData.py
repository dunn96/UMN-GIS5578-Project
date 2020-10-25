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
water2014.rename(columns = {"WATER_NAME" : "NAME"})