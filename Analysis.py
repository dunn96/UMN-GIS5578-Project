import geopandas as gpd

water2014 = gpd.read_file("water2014_clip.shp")

water2014_buffer = gpd.GeoDataFrame(water2014.buffer(500))
water2014_buffer["NAME"] = water2014["NAME"]
water2014_buffer = water2014_buffer.set_geometry(water2014_buffer[0])
water2014_buffer = water2014_buffer[["NAME", "geometry"]]