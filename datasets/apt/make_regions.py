import csv
import geopandas as gpd
import pandas as pd
from shapely.geometry import shape
from shapely import set_precision
import json
from rdflib import Graph, URIRef, BNode, Literal, Namespace
from rdflib.namespace import DCTERMS, GEO, PROV, RDF, RDFS, SDO, SKOS, XSD


def ms_check():
    # map_index = gpd.read_file("source/250k_MapSheetDataIndex/TopographicMapsIndex_250k.shp")
    # map_index[["mapnumber"]].to_csv("source/MapIndex-numbers.csv")

    regions = pd.read_csv("source/Regions-MS-check.csv")
    map_index = pd.read_csv("source/MapIndex-numbers.csv")
    # regions["InMsIndex"] = regions.apply(lambda x: regions.MapSheet in map_index.MapSheet, axis=1)
    # regions.to_csv("source/Regions-MS-check2.csv")
    regions["Exists"] = regions.MapSheet.isin(map_index.MapSheet)
    regions.to_csv("source/Regions-MS-check.csv")


def get_regions_polygons():
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
    result = pd.merge(map_index, regions, how="left", left_on="mapnumber", right_on="MapSheet")
    # print(result.columns)
    # """
    # Index(['objectid', 'featuretyp', 'layoutguid', 'mapname', 'mapnumber',
    #    'revised', 'gaid', 'editcode', 'globalid', 'map_title', 'year_publi',
    #    'mapnumber_', 'edition', 'pid_url', 'index_', 'st_area_sh',
    #    'st_perimet', 'geometry', 'Region', 'Map number'],
    #   dtype='object')
    # """
    reduced_result = result[["Region", "MapSheet", "geometry"]]

    REGIONS_IRIS = json.load(open("source/Regions-IRIs.json"))

    with open("source/Regions.csv", "w") as f:
        wr = csv.writer(f)
        wr.writerow(["IRI", "Region", "WKT"])
        for i, row in reduced_result.iterrows():
            if str(row["Region"]) != "nan":
                region_iri = URIRef(REGIONS_IRIS[str(row["Region"])])
                wr.writerow([region_iri, row["Region"], shape(row["geometry"]).buffer(0)])


def make_rdf():
    REGIONS_IRIS = json.load(open("source/Regions-IRIs.json"))

    # setup graph
    g = Graph()
    DS = Namespace("https://data.idnau.org/pid/apt/")
    g.bind("", DS)
    regions_iri = DS.regions

    regions = gpd.read_file("source/Regions/Regions.shp")
    print(regions.columns)
    # Index(['IRI', 'Region', 'geometry'], dtype='object')
    print(regions.shape)
    # (82, 3)

    for index, row in regions.iterrows():
        region_iri = URIRef(str(row["IRI"]))
        g.add((region_iri, RDF.type, GEO.Feature))
        if region_iri == URIRef("https://data.idnau.org/pid/apt/nsw-sydney"):
            g.add((region_iri, SDO.name, Literal("Sydney")))
        else:
            g.add((region_iri, SDO.name, Literal(str(row["Region"]))))
        g.add((regions_iri, RDFS.member, region_iri))

        # Geometry
        geom = BNode()
        g.add((region_iri, GEO.hasGeometry, geom))
        g.add((geom, RDF.type, GEO.Geometry))
        wkt = set_precision(shape(row["geometry"]).buffer(0), 0.00001)
        g.add((geom, GEO.asWKT, Literal(wkt, datatype=GEO.wktLiteral)))

    g.serialize(destination="source/rdf/regions.ttl", format="longturtle")


if __name__ == "__main__":
    # ms_check()
    # get_regions_polygons()
    make_rdf()
