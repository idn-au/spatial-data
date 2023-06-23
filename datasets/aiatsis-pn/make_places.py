import csv
import re

import geopandas as gpd
import pandas as pd
from shapely.geometry import shape


def process_places():
    """This function tidies up the Places.csv file which was exported from the Places-as-received.csv file
    obtained from AIATSIS which is a raw export of Place Names. This function presents neat MapSheet numbers
    for places, one per row."""
    with open("source/Places2.csv", "w") as f2:
        wr = csv.writer(f2)
        wr.writerow(["Place", "Region", "MapSheet", "Is250"])
        with open("source/Places.csv") as f:
            for row in csv.reader(f):
                m = re.findall(r"(S[A-Z][0-9]{2}([\-][0-9]{2})?)", row[0])
                map_sheets = []
                if m is not None:
                    for ms in m:
                        map_sheets.append(ms[0].replace("-", "")[1:])
                else:
                    map_sheets = []

                for map_sheet in map_sheets:
                    m2 = re.findall(r"([A-Z][0-9]{4})", map_sheet)
                    twofifty = False
                    if len(m2) > 0:
                        twofifty = True
                    wr.writerow(row + [map_sheet] + ["Y" if twofifty else "N"])
    print("Done")


def join_places_to_geoms():
    """This function reads the tidied-up Places2.csv file output from process_places() and produced Places3.csv which
    contains WKT geoemetrieps per MapSheet by joining on to the Mapsheet index dataset obtained from GA.

    Merging of the MapSheets into one geometry per Place is done in QGIS with the Dissolve command, not in Python.

    WARNING: the file generated is ~500MB"""
    places = pd.read_csv("source/Places2.csv")
    map_index = gpd.read_file("source/250k_MapSheetDataIndex/TopographicMapsIndex_250k.shp")
    result = pd.merge(map_index, places, how="left", left_on="mapnumber", right_on="MapSheet")
    reduced_result = result[["Place", "Region", "MapSheet", "geometry"]]
    with open("source/Places3.csv", "w") as f:
        wr = csv.writer(f)
        wr.writerow(["Place", "MapSheet", "WKT"])
        for i, row in reduced_result.iterrows():
            wr.writerow([row["Place"], row["MapSheet"], shape(row["geometry"]).buffer(0)])


if __name__ == "__main__":
    join_places_to_geoms()
