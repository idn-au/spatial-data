import geopandas as gpd
import pandas as pd
from shapely.geometry import shape


if __name__ == "__main__":
    """Joins Regions in a slightly altered version of the Regions data received from AIATSIS in Regions-as-recieved.xlsx
    to MapSheet polygons in the Mapsheet index obtained from GA.
    
    Results output in Regions2.csv contain one MapSheet number & polygon per row with Region names duplicated to 
    indicate multiple MapSheets per Region.
    
    Merging of the MapSheets into one geometry per Region is done in QGIS with the Dissolve command, not in Python. 
    
    WARNING: resultant file is 43MB"""
    # Join Regions and TopoIndex
    # extract only needed columns
    regions = pd.read_excel("source/Regions-as-received.xlsx", sheet_name="Map Numbers")
    map_index = gpd.read_file("source/250k_MapSheetDataIndex/TopographicMapsIndex_250k.shp")
    result = pd.merge(map_index, regions, how="left", on="mapnumber")
    # print(result.columns)
    # """
    # Index(['objectid', 'featuretyp', 'layoutguid', 'mapname', 'mapnumber',
    #    'revised', 'gaid', 'editcode', 'globalid', 'map_title', 'year_publi',
    #    'mapnumber_', 'edition', 'pid_url', 'index_', 'st_area_sh',
    #    'st_perimet', 'geometry', 'Region', 'Map number'],
    #   dtype='object')
    # """
    reduced_result = result[["Region", "mapnumber", "geometry"]]
    with open("source/Regions2.csv", "w") as f:
        f.write("Region,MapSheet,WKT\n")
        for i, row in reduced_result.iterrows():
            f.write(f'{row["Region"]},{row["mapnumber"]},"{shape(row["geometry"]).buffer(0)}"\n')
