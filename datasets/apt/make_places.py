import csv
import os
import re

import geopandas as gpd
import pandas as pd
from shapely import set_precision
from shapely.geometry import shape

import time
import json
from rdflib import Graph, URIRef, BNode, Literal, Namespace
from rdflib.namespace import DCTERMS, GEO, PROV, RDF, RDFS, SDO, SKOS, XSD

REGION_IRIS = {
    "ACT, S NSW": "https://data.idnau.org/pid/apt/act-s-nsw",
    "Arnhem Land NT": "https://data.idnau.org/pid/apt/arnhem-land-nt",
    "Bamaga Qld Far North Cape York": "https://data.idnau.org/pid/apt/bamaga-qld-far-north-cape-york",
    "Central Arnhem Land NT": "https://data.idnau.org/pid/apt/central-arnhem-land-nt",
    "Central NT": "https://data.idnau.org/pid/apt/central-nt",
    "Central NT Tanami Desert": "https://data.idnau.org/pid/apt/central-nt-tanami-desert",
    "Central NT Tanami Desert, North NT": "https://data.idnau.org/pid/apt/central-nt-tanami-desert-north-nt",
    "Central NT, North NT": "https://data.idnau.org/pid/apt/central-nt-north-nt",
    "Central WA": "https://data.idnau.org/pid/apt/central-wa",
    "Central WA Great Sandy Desert": "https://data.idnau.org/pid/apt/central-wa-great-sandy-desert",
    "Central WA Tanami Desert": "https://data.idnau.org/pid/apt/central-wa-tanami-desert",
    "Central WA Warburton": "https://data.idnau.org/pid/apt/central-wa-warburton",
    "E Qld": "https://data.idnau.org/pid/apt/e-qld",
    "E Tas": "https://data.idnau.org/pid/apt/e-tas",
    "E Vic": "https://data.idnau.org/pid/apt/e-vic",
    "E Vic Gippsland": "https://data.idnau.org/pid/apt/e-vic-gippsland",
    "East Arnhem Land NT": "https://data.idnau.org/pid/apt/east-arnhem-land-nt",
    "East Kimberley WA": "https://data.idnau.org/pid/apt/east-kimberley-wa",
    "Elcho Island East Arnhem Land NT": "https://data.idnau.org/pid/apt/elcho-island-east-arnhem-land-nt",
    "Far West SA": "https://data.idnau.org/pid/apt/far-west-sa",
    "Far West SA Nullarbor": "https://data.idnau.org/pid/apt/far-west-sa-nullarbor",
    "Gibson Desert WA": "https://data.idnau.org/pid/apt/gibson-desert-wa",
    "Great Sandy Desert WA": "https://data.idnau.org/pid/apt/great-sandy-desert-wa",
    "Little Sandy Desert WA": "https://data.idnau.org/pid/apt/little-sandy-desert-wa",
    "Mainland North NT": "https://data.idnau.org/pid/apt/mainland-north-nt",
    "Mainland Qld Gulf": "https://data.idnau.org/pid/apt/mainland-qld-gulf",
    "N NSW": "https://data.idnau.org/pid/apt/n-nsw",
    "N Vic": "https://data.idnau.org/pid/apt/n-vic",
    "N Vic, SW NSW": "https://data.idnau.org/pid/apt/n-vic-sw-nsw",
    "NE Qld": "https://data.idnau.org/pid/apt/ne-qld",
    "NE SA": "https://data.idnau.org/pid/apt/ne-sa",
    "NE SA Flinders Ranges": "https://data.idnau.org/pid/apt/ne-sa-flinders-ranges",
    "NE Tas": "https://data.idnau.org/pid/apt/ne-tas",
    "North NT": "https://data.idnau.org/pid/apt/north-nt",
    "North NT Roper": "https://data.idnau.org/pid/apt/north-nt-roper",
    "North West Central SA": "https://data.idnau.org/pid/apt/north-west-central-sa",
    "NSW": "https://data.idnau.org/pid/apt/nsw",
    "NSW Far S Coast": "https://data.idnau.org/pid/apt/nsw-far-s-coast",
    "NSW N Coast": "https://data.idnau.org/pid/apt/nsw-n-coast",
    "NSW S Coast": "https://data.idnau.org/pid/apt/nsw-s-coast",
    "NT Top End": "https://data.idnau.org/pid/apt/nt-top-end",
    "NT Top End Roper": "https://data.idnau.org/pid/apt/nt-top-end-roper",
    "NW NSW": "https://data.idnau.org/pid/apt/nw-nsw",
    "NW Tas": "https://data.idnau.org/pid/apt/nw-tas",
    "NW Vic": "https://data.idnau.org/pid/apt/nw-vic",
    "Qld Far North, NE Cape York": "https://data.idnau.org/pid/apt/qld-far-north-ne-cape-york",
    "Qld Far North, NE Cape York, Qld Gulf": "https://data.idnau.org/pid/apt/qld-far-north-ne-cape-york-qld-gulf",
    "Qld Far NW": "https://data.idnau.org/pid/apt/qld-far-nw",
    "Qld Far NW Barkly Tableland": "https://data.idnau.org/pid/apt/qld-far-nw-barkly-tableland",
    "Qld Far West": "https://data.idnau.org/pid/apt/qld-far-west",
    "Qld Gulf": "https://data.idnau.org/pid/apt/qld-gulf",
    "Qld NE Cape York": "https://data.idnau.org/pid/apt/qld-ne-cape-york",
    "Qld NW Cape York": "https://data.idnau.org/pid/apt/qld-nw-cape-york",
    "Qld SE Cape York": "https://data.idnau.org/pid/apt/qld-se-cape-york",
    "Qld TSI": "https://data.idnau.org/pid/apt/qld-tsi",
    "S NSW": "https://data.idnau.org/pid/apt/s-nsw",
    "SA Central Australia": "https://data.idnau.org/pid/apt/sa-central-australia",
    "SE Central NT": "https://data.idnau.org/pid/apt/se-central-nt",
    "SE Central NT Simpson Desert": "https://data.idnau.org/pid/apt/se-central-nt-simpson-desert",
    "SE Qld": "https://data.idnau.org/pid/apt/se-qld",
    "SE SA": "https://data.idnau.org/pid/apt/se-sa",
    "SE Tas": "https://data.idnau.org/pid/apt/se-tas",
    "SE WA": "https://data.idnau.org/pid/apt/se-wa",
    "SE WA Goldfields": "https://data.idnau.org/pid/apt/se-wa-goldfields",
    "SE WA Great Victoria Desert": "https://data.idnau.org/pid/apt/se-wa-great-victoria-desert",
    "SE WA Nullarbor": "https://data.idnau.org/pid/apt/se-wa-nullarbor",
    "South Central NT": "https://data.idnau.org/pid/apt/south-central-nt",
    "SW NSW": "https://data.idnau.org/pid/apt/sw-nsw",
    "SW Qld": "https://data.idnau.org/pid/apt/sw-qld",
    "SW Tas": "https://data.idnau.org/pid/apt/sw-tas",
    "SW WA": "https://data.idnau.org/pid/apt/sw-wa",
    "Tas Bass Strait": "https://data.idnau.org/pid/apt/tas-bass-strait",
    "Vic": "https://data.idnau.org/pid/apt/vic",
    "Victoria River, North NT": "https://data.idnau.org/pid/apt/victoria-river-north-nt",
    "W Tas": "https://data.idnau.org/pid/apt/w-tas",
    "W Vic": "https://data.idnau.org/pid/apt/w-vic",
    "WA": "https://data.idnau.org/pid/apt/wa",
    "WA East Kimberley": "https://data.idnau.org/pid/apt/wa-east-kimberley",
    "WA East Pilbara": "https://data.idnau.org/pid/apt/wa-east-pilbara",
    "WA Fitzroy River, West Kimberley": "https://data.idnau.org/pid/apt/wa-fitzroy-river-west-kimberley",
    "WA Gascoyne / Murchison": "https://data.idnau.org/pid/apt/wa-gascoyne-murchison",
    "WA South Pilbara / Gascoyne": "https://data.idnau.org/pid/apt/wa-south-pilbara-gascoyne",
    "WA West Kimberley": "https://data.idnau.org/pid/apt/wa-west-kimberley",
    "WA West Pilbara": "https://data.idnau.org/pid/apt/wa-west-pilbara",
    "West Arnhem Land NT": "https://data.idnau.org/pid/apt/west-arnhem-land-nt",
    "West SA": "https://data.idnau.org/pid/apt/west-sa"
}


def ms_check():
    # map_index = gpd.read_file("source/250k_MapSheetDataIndex/TopographicMapsIndex_250k.shp")
    # map_index[["mapnumber"]].to_csv("source/MapIndex-numbers.csv")

    regions = pd.read_csv("source/Regions-MS-check.csv")
    map_index = pd.read_csv("source/MapIndex-numbers.csv")
    # regions["InMsIndex"] = regions.apply(lambda x: regions.MapSheet in map_index.MapSheet, axis=1)
    # regions.to_csv("source/Regions-MS-check2.csv")
    regions["Exists"] = regions.MapSheet.isin(map_index.MapSheet)
    regions.to_csv("source/Regions-MS-check.csv")


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
    contains WKT geoemetries per MapSheet by joining on to the Mapsheet index dataset obtained from GA.

    Merging of the MapSheets into one geometry per Place is done in QGIS with the Dissolve command, not in Python.

    WARNING: the file generated is ~500MB"""
    places = pd.read_csv("source/Places-reduced8.csv")
    map_index = gpd.read_file("source/250k_MapSheetDataIndex/TopographicMapsIndex_250k.shp")
    result = pd.merge(map_index, places, how="left", left_on="mapnumber", right_on="MapSheet")
    with open("source/Places8.csv", "w") as f:
        wr = csv.writer(f)
        wr.writerow(["Place", "Parent", "UseFor", "Broader", "MapSheet", "WKT"])
        for i, row in result.iterrows():
            wr.writerow([row["Place"], row["Parent"], row["UF"], row["BT"], row["MapSheet"], shape(row["geometry"]).buffer(0)])


def tidy_place_shp_names():
    start_time = time.time()
    places = gpd.read_file("source/Places/Places.shp")
    print(places.head()[["Place"]])
    # add a Region column
    places["Region"] = places.loc[:, "Place"]

    # split Place column into tidy Place & region
    for index, row in places.iterrows():
        p = row["Place"].split("(")[0].strip()
        places.loc[index, ["Place"]] = p
        r = row["Place"].split("(")
        r = r[1].strip(" ()") if len(r) > 1 else r[0]
        r = r[:-8]
        places.loc[index, ["Region"]] = r

    places[["Place", "Region"]].to_csv("source/Places4.1.csv")
    # os.mkdir("source/Places2")
    places.to_file("source/Places2/Places.shp")
    places2 = gpd.read_file("source/Places2/Places.shp")
    print(places2[["Place", "Region"]].head())

    print("--- %s seconds ---" % (time.time() - start_time))


def process_places_reduced():
    map_index = pd.read_csv("source/MapIndex-numbers.csv")

    with open("source/Places-reduced3.csv", "w") as f2:
        wr = csv.writer(f2)
        wr.writerow(["Place", "MapSheets", "MsExists", "UF", "BT"])
        with open("source/Places-reduced2.csv") as f:
            for row in csv.reader(f):
                m = re.findall(r"(S[A-Z][0-9]{2}([\-][0-9]{2})?)", row[0])
                map_sheets = []
                ms_exists = []
                if m is not None:
                    for ms in m:
                        tidy_ms = ms[0].replace("-", "")[1:]
                        map_sheets.append(tidy_ms)
                        if tidy_ms in map_index.MapSheet.values:
                            ms_exists.append("1")
                        else:
                            ms_exists.append("0")
                else:
                    map_sheets = []

                wr.writerow([row[0], ";".join(map_sheets), ";".join(ms_exists), row[3], row[4]])
    print("Done")


def separate_place_name():
    with open("source/Places-reduced4.csv", "w") as f2:
        wr = csv.writer(f2)
        wr.writerow(["Place", "Parent", "MapSheets", "MsExists", "UF", "BT"])
        with open("source/Places-reduced3.csv") as f:
            for row in csv.reader(f):
                print(row[0])
                new_row = []
                if "(" in row[0]:
                    new_row.append(row[0].split("(")[0].strip())
                    new_row.append(row[0].split("(")[1].strip(" )"))
                else:
                    new_row.append(row[0])
                    new_row.append("")
                new_row.append(row[1])
                new_row.append(row[2])
                new_row.append(row[3])
                new_row.append(row[4])
                print(new_row)
                wr.writerow(new_row)


def clean_parent():
    with open("source/Places-reduced5.csv", "w") as f2:
        wr = csv.writer(f2)
        wr.writerow(["Place", "Parent", "CleanParent", "MapSheets", "MsExists", "UF", "BT"])
        with open("source/Places-reduced4.csv") as f:
            for row in csv.reader(f):
                m = re.sub(r"\sS[A-Z][0-9]{2}-[0-9]{2}", row[1])
                if m is not None:
                    cp = row[1][:-8]
                else:
                    cp = ""

                m = re.search(r"\sS[A-Z][0-9]{2}-[0-9]{2},[\s]?$", cp)
                if m is not None:
                    cp = cp.strip()[:-8]

                m = re.search(r"\sS[A-Z][0-9]{2}-[0-9]{2},[\s]?$", cp)
                if m is not None:
                    cp = cp.strip()[:-8]

                new_row = [row[0], row[1], cp, row[2], row[3], row[4], row[5]]

                wr.writerow(new_row)


def get_distinct_clean_parents():
    parents = set()
    with open("source/Places-reduced5.csv") as f:
        for row in csv.reader(f):
            parents.add(row[2])
    with open("source/Parents.csv", "w") as f2:
        wr = csv.writer(f2)
        wr.writerow(["Parent"])
        for p in sorted(parents):
            wr.writerow([p])


def spread_out_multisheets():
    with open("source/Places-reduced6.csv", "w") as f2:
        wr = csv.writer(f2)
        wr.writerow(["Place", "CleanParent", "MapSheet", "UF", "BT"])
        with open("source/Places-reduced5.csv") as f:
            for row in csv.reader(f):
                if "1" in row[4]:
                    mapsheets = row[3].split(";")
                    exists = row[4].split(";")
                    for i, e in enumerate(exists):
                        if e == "1":
                            wr.writerow([row[0], row[2], mapsheets[i], row[5], row[6]])


def clean_uf():
    with open("source/Places-reduced7.csv", "w") as f2:
        wr = csv.writer(f2)
        wr.writerow(["Place", "Parent", "MapSheets", "UF", "UF Clean", "BT"])
        with open("source/Places-reduced6.csv") as f:
            for row in csv.reader(f):
                wr.writerow([row[0], row[1], row[2], row[3], re.sub(r"\s\(([^\;]+)\)", "", row[3]), row[4]])


def make_regions_iris():
    for k, v in REGION_IRIS.items():
        REGION_IRIS[k] = v + k.lower().replace(" ", "-").replace(",", "").replace("/", "-").replace("---", "-")

    json.dump(REGION_IRIS, open("source/Regions-IRIs.json", "w"), indent=4)


def make_place_iri(place_name):
    iri = str(place_name).lower().replace(" ", "-").replace(",", "").replace("/", "-").replace("---", "-")

    return URIRef("https://data.idnau.org/pid/apt/" + iri)


def make_rdf():
    REGIONS_IRIS = json.load(open("source/Regions-IRIs.json"))

    # setup graph
    g = Graph()
    DS = Namespace("https://data.idnau.org/pid/apt/")
    g.bind("", DS)
    places_iri = DS.places

    places = gpd.read_file("source/Places/Places.shp")
    print(places.columns)
    # Index(['Place', 'Parent', 'UseFor', 'Broader', 'geometry'], dtype='object')
    print(places.shape)
    # (5871, 5)

    REPLACEMENT_REGIONS = {
        'Adelaide SA': None,
        'Alice Springs South Central NT': None,
        'Angas Hills, Central WA Great Sandy Desert': 'Central WA Great Sandy Desert',
        'Arnhem Land, NT': 'North NT',
        'Avon River SW WA': None,
        'Bathurst Island NT': 'SW WA',
        'Bellarine Peninsula Vic': 'Vic',
        'Blue Mountains W Sydney NSW': None,
        'Botany Bay S Sydney NSW': 'N Sydney NSW',
        'Brisbane SE Qld': None,
        'Buccaneer, WA West Kimberley': 'WA West Kimberley',
        'Buchan, E Vic Gippsland': 'E Vic Gippsland',
        'Bundaberg map area SE Qld': None,
        'Burketown, Qld Gulf': 'Qld Gulf',
        'Canberra ACT': None,
        'Canberrra ACT': None,
        'Cape Otway W Vic': None,
        'Cape Schanck, Mornington Peninsula Vic': 'Vic',
        'Carnarvon Range SW Qld': None,
        'Central Arnhem Land': None,
        'Central NT Tanami Desert SF52-11, Central WA': 'Central WA',
        'Central Sydney NSW': 'N Sydney NSW',
        'Central WA Warburton, NT': 'North NT',
        'Condobolin SW NSW': None,
        'Condobolin, SW NSW': 'SW NSW',
        'Coonabarabran N NSW': None,
        'Coonamble, N NSW': 'N NSW',
        'Cowra, SW NSW': 'SW NSW',
        'Cox Peninsula NT Top End': None,
        'Cox River, North NT': 'North NT',
        'Crocodile Islands Central Arnhem Land': None,
        'Croker Island West Arnhem Land NT': None,
        'Daly River NT Top End': None,
        'Darwin NT Top End': None,
        'Devonport, NW Tas': 'NW Tas',
        'E Sydney NSW': 'N Sydney NSW',
        'E Vic La Trobe Valley': None,
        'E Vic SJ55-03, NSW Far S Coast SJ55-04, E Vic Gippsland': 'Vic',
        'E Vic Yarra Valley': None,
        'East Arnhem Land': None,
        'East Kimberley, North NT': 'North NT',
        'Far West Nullarbor SA': None,
        'Far West SA Nullarbor SH52-16, Nullarbor': 'Far West SA Nullarbor',
        'Fitzmaurice River NT Top End': None,
        'Fitzroy River, WA East Kimberley': 'WA East Kimberley',
        'Fleurieu Peninsula SE SA': None,
        'Forster, SE SA': 'SE SA',
        'Fraser Island, SE Qld': 'SE Qld',
        'Gariwerd / Grampians W Vic': None,
        'Grampians W Vic': None,
        'Griffith SW NSW': None,
        'Griffith, SW NSW': 'SW NSW',
        'Groote Eylandt NT Gulf Islands': None,
        'Hawkesbury NSW': None,
        'Hunter Island, Bass Strait NW Tas': 'Tas Bass Strait',
        'Inner east Sydney': 'N Sydney NSW',
        'Inner south Sydney NSW': 'N Sydney NSW',
        'Inner Sydney NSW': 'N Sydney NSW',
        'Inner west Sydney NSW': 'N Sydney NSW',
        'James Ranges South Central NT': None,
        'Jervis Bay ACT / NSW S Coast': None,
        'Kakadu NT': None,
        'Kakadu, NT': 'North NT',
        'Kangaroo Island SE SA': None,
        'Kempsey, NSW N Coast': 'NSW N Coast',
        'Laura Qld SE Cape York': None,
        'Laverton, SE WA': 'SE WA',
        'Mallacoota map area': None,
        'Melbourne Vic': None,
        'Melbourne Vic SJ55-05, E Vic': 'E Vic',
        'Melville Island NT': None,
        'Mersey NW Tas': None,
        'Mid West WA': None,
        'Moa / Banks Island Qld TSI': None,
        'Moa Island Qld TSI': None,
        'Monaro, S NSW': 'S NSW',
        'Moreton Bay, SE Qld': 'SE Qld',
        'Mornington Island Qld Wellesley Gulf Islands': None,
        'Mornington Peninsula Vic': None,
        'N Melbourne Vic': None,
        'N NSW SH55-11,': None,
        'N NSW, SW Qld': 'SW Qld',
        'N Qld': None,
        'N SA': None,
        'N Sydney': 'N Sydney NSW',
        'N Sydney area NSW': 'N Sydney NSW',
        'Namadgi ACT': None,
        'Nambucca, NSW N Coast': 'NSW N Coast',
        'nan': None,
        'Narrandera, SW NSW': 'SW NSW',
        'NE QLD': None,
        'NE Qld SE54-04,': None,
        'NE Sydney': 'N Sydney NSW',
        'North NT Barkly Tablelands': None,
        'North NT Victoria River': None,
        'Northern Territory NT': None,
        'Nourlangie, Kakadu, NT': 'North NT',
        'NT': None,
        'NT Groote Eylandt NT Gulf Islands': None,
        'NT Gulf Islands': None,
        'NT Top End Upper Roper': None,
        'NT Upper Roper': None,
        'NW Vic Murray River': None,
        'Outstation Central Arnhem Land NT': None,
        'Outstation, Central Arnhem Land NT': 'Central Arnhem Land NT',
        'Palm Islands NE Qld': None,
        'Penrith, W Sydney NSW': 'N Sydney NSW',
        'Percival Lakes Great Sandy Desert WA': None,
        'Perth SW WA': None,
        'Qld': None,
        'Qld Far North Cape York': None,
        'Qld Far West SF54-09, SF54-13, SE Central NT': 'SE Central NT',
        'Qld Gulf Islands': None,
        'Qld Gulf Wellesley Islands': None,
        'Qld Gulf, NW Cape York': 'Qld NW Cape York',
        'Qld SE Cape York Flinders Group': None,
        'Qld Townsville': None,
        'Qld TSI SC54,': None,
        'Rocky Cape, NW Tas': 'NW Tas',
        'Royal National Park, S Sydney NSW': 'N Sydney NSW',
        'S Sydney NSW': 'N Sydney NSW',
        'S Vic Melbourne': None,
        'SA': None,
        'SA Central Australia SG52-11, South Central NT': 'South Central NT',
        'SC52-16, SC 53-13,': None,
        'SE Adelade SA': None,
        'SE Melbourne': None,
        'SE SA Kangaroo Island': None,
        'SE Vic': None,
        'SE WA Nullabor': None,
        'Snowy S NSW': None,
        'South Central NT SG52-07, WA': 'WA',
        'South Goulburn Island West Arnhem Land NT': None,
        'SW Melbourne': None,
        'SW Melbourne Vic': None,
        'SW NSW / N Vic': None,
        'SW NSW Murray River': None,
        'Sydney': 'N Sydney NSW',
        'Sydney area NSW': 'N Sydney NSW',
        'Sydney NSW': 'NSW N Coast',
        'Taree, NSW N Coast': 'NSW N Coast',
        'Tas': None,
        'Tidbinbilla ACT': 'ACT, S NSW',
        'Uluru, South Central NT': 'South Central NT',
        'Vic Melbourne': 'Vic',
        'Victoria River Downs North NT': 'North NT',
        'W NSW': 'SW NSW',
        'W Papua PNG': None,
        'W Perth': 'SW WA',
        'W Sydney': 'N Sydney NSW',
        'W Sydney NSW': 'N Sydney NSW',
        'W Vic Gariwerd / Grampians': 'W Vic',
        'WA Drysdale East Kimberley': 'WA East Kimberley',
        'Wa East Pilbara': 'WA East Pilbara',
        'WA Forrest East Kimberley': 'WA East Kimberley',
        'WA Gascoyne/Murchison': 'WA Gascoyne / Murchison',
        'WA Pilbara': 'WA East Pilbara',
        'WA South Pilbara': 'WA South Pilbara / Gascoyne',
        'Weipa, Qld NW Cape York': 'Qld NW Cape York',
        'West SA SI53-06,': 'West SA',
        'Western Port Vic': 'Vic',
        'Whitsundays E Qld': 'E Qld',
        'Willandra NW NSW': 'NW NSW',
        'Willandra SW NSW': 'SW NSW',
        'Willeroo, North NT': 'North NT',
        'Wintinna map area': None,
    }

    for index, row in places.iterrows():
        place_iri = make_place_iri(row["Place"])

        parent_iri = None
        p = str(row["Parent"])
        if p in REGIONS_IRIS.keys():
            parent_iri = URIRef(REGIONS_IRIS[p])
        else:
            if p in REPLACEMENT_REGIONS.keys():
                if REPLACEMENT_REGIONS[p] is not None:
                    try:
                        parent_iri = URIRef(REGIONS_IRIS[REPLACEMENT_REGIONS[p]])
                    except KeyError:
                        print(f"Missing {p}")

        if parent_iri is not None:
            g.add((place_iri, GEO.sfWithin, parent_iri))
        else:
            g.add((place_iri, SDO.description, Literal(f"Within {p}")))

        g.add((place_iri, RDF.type, GEO.Feature))
        g.add((place_iri, SDO.name, Literal(str(row["Place"]))))
        g.add((places_iri, RDFS.member, place_iri))

        if not pd.isnull(row["UseFor"]):
            if not row["UseFor"] == "nan":
                g.add((place_iri, SKOS.altLabel, Literal(str(row["UseFor"]))))

        # Geometry
        geom = BNode()
        g.add((place_iri, GEO.hasGeometry, geom))
        g.add((geom, RDF.type, GEO.Geometry))
        wkt = set_precision(shape(row["geometry"]).buffer(0), 0.00001)
        g.add((geom, GEO.asWKT, Literal(wkt, datatype=GEO.wktLiteral)))

    g.serialize(destination="source/rdf/places.ttl", format="longturtle")


def make_rdf_nq():
    pass


if __name__ == "__main__":
    # join_places_to_geoms()
    # tidy_place_shp_names()
    # process_places_reduced()
    # separate_place_name()
    # clean_parent()
    # get_distinct_clean_parents()
    # spread_out_multisheets()
    # clean_uf()
    # join_places_to_geoms()
    # make_regions_iris()
    # make_rdf()
    make_rdf()
