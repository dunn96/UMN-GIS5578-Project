# Foot Traffic and Water Quailty Analysis

## Introductory information
### Contact
* Author: Nicole Dunn, dunnx219@umn.edu
* Author: Maisong Francis, leex6165@umn.edu 
 
### Files
* Analysis.py
    * Format: Python file
    * Description: This script performs spatial analysis with the impaired water dataset and the SafeGraph and outputs statistical metrics. 
 
* Waterdata.py
    * Format: Python file
    * Description: This script manipulates and cleans the four impaired water datasets and the hydrography dataset and reduces them to the seven county metropolitan MN area using pandas and geopandas.
 
* SafeGraph.py
    * Format: Python file
    * Description: This script manipulates, reduces, and geocodes the SafeGraph dataset to the seven county metropolitan MN area using glob, gzip, pandas, and arcpy. 
 
* Impaired_2014_lakes.zip - Impaired water dataset
    * Source: MPCA - https://gisdata.mn.gov/dataset/env-impaired-water-2014 
    * Format: Zipped Shapefile
    * Description: This is a polygon dataset of the impaired lakes within Minnesota for the year 2014 and any preceding years useless they were delisted.
 
* Impaired_2016_lakes.zip - Impaired water dataset
    * Source: MPCA - https://gisdata.mn.gov/dataset/env-impaired-water-2016 
    * Format:Zipped Shapefile
    * Description: This is a polygon dataset of the impaired lakes within Minnesota for the year 2016 and any preceding years useless they were delisted.
 
* Impaired_2018_lakes.zip - Impaired water dataset
    * Source: MPCA - https://gisdata.mn.gov/dataset/env-impaired-water-2018 
    * Format:Zipped Shapefile
    * Description:This is a polygon dataset of the impaired lakes within Minnesota for the year 2018 and any preceding years useless they were delisted.
 
* wq-iw1-65.csv
    * Source: MPCA - https://www.pca.state.mn.us/water/minnesotas-impaired-waters-list 
    * Format: CSV File
    * Description:This is a draft list of all impaired waterbodies within Minnesota for the year 2020 and any preceding years useless they were delisted.
 
* shp_bdry_metro_counties_and_ctus.zip
    * Source: Metropolitan Council - https://gisdata.mn.gov/dataset/us-mn-state-metc-bdry-metro-counties-and-ctus 
    * Format: Zipped Shapefile
    * Description: This is a polygon dataset for the county boundaries within the Twin Cities seven county metropolitan area. The dataset also contains city, township and unorganized territory (CTU) boundaries. 
 
* shp_water_dnr_hydrography.zip
    * Source: DNR - https://gisdata.mn.gov/dataset/water-dnr-hydrography 
    * Format:Zipped Shapefile
    * Description: This is a polygon dataset representing the Minnesota surficial hydrology. 
        * Will be replaced by National Wetlands Inventory update (2009-2014) upon its completion in 2020

* <mmm><yy>patterns-part?.csv.gz
    * Source: SafeGraph
    * Format: csv.gz
    * Description: Foot traffic patterns for the United States. Collected from April 2019 through Sep 2020

## Installation 
* Used a combination of Jupyterlab and Jupyter Notebooks (with ArcPro)
* Anaconda was used for the package manager
* Pandas, Geopandas, Glob, Gzip, Arcpy (Business analyst and spatial analyst extension)

## Methodological information / Usage
Method description, links or references to publications or other documentation containing experimental design or protocols used in data collection
Describe any quality-assurance procedures performed on the data
Characterize low quality/questionable/outliers that people should be aware
 
Sharing and Access information
Licenses or restrictions placed on the data (ArcPy)
