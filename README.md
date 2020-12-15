# Foot Traffic and Water Quailty Analysis

## Introductory information
### Contact
* Author: Nicole Dunn, dunnx219@umn.edu
* Author: Maisong Francis, leex6165@umn.edu 
 
### Files
* Analysis.py
    * Format: Python file
    * Description: This script performs spatial analysis with the impaired water dataset and the SafeGraph and outputs statistical metrics. 

* Functions.py
    * Format: Python file
    * Description: This file contains the functions meant to be used within the Analysis.py script

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

* mmmyypatterns-part?.csv.gz
    * Source: SafeGraph
    * Format: csv.gz
    * Description: Foot traffic patterns for the United States. Collected from apr19 through sep20. There are three-four files for each month     represented by '?' 
    * Example: jan19patterns-part1.csv.gz
    
* spec-file.txt
    * Description: Describes the Python environment. 

## Installation 
* Used a combination of Jupyterlab and Jupyter Notebooks (with ArcPro)
* Anaconda was used for the package manager
* Pandas, Geopandas, Glob, Gzip, Arcpy (Business analyst and spatial analyst extension)

## Methodological information / Usage
This project contains 4 scripts. The first script (WaterData.py) cleans spatial data files relating to the water data
that will be used in future analysis. Cleaning the data includes clipping all the data to the seven county metro as 
the area of interest, removing fields that are not needed, removing invalid geometries from the geodataframes, 
and adding geometry where there is none. Thes second script (SafeGraph.py) reduces tabular monthly SafeGraph patterns 
to the seven metropolitan counties in Minnesota. The multiple SafeGraph files for each month are also reduced to schema 
of interest through index and combined into one file per month. This script also geocodes the points of interest within 
the seven metropolitan counties. The third script (Analysis.py) This script is designed to be used after WaterData.py and 
SafeGraph.py. This script buffers lake features based on user input and gets visitation counts within each lake buffer. 
The results are statistical outputs of visitation counts per month and year for each category of impairment status: impaired and 
nonimpaired, and prints top five most and least visited lakes for each year. The script also prints the removed and added 
lakes between each biennial impaired waters dataset. The fourth script (Functions.py) contains the functions used within the 
Analysis.py script and is imported as a module in the Analysis.py file.
