from pathlib import Path
from rdflib import Graph, URIRef, BNode, Literal, Namespace
from rdflib.namespace import DCTERMS, GEO, RDF, RDFS, SDO, XSD
import geopandas as gpd
from pyshacl import validate
import shapely
import json

if __name__ == "__main__":
    # setup graph
    g = Graph()
    dataset_iri = URIRef("https://data.idnau.org/pid/nntt")
    DS = Namespace(str(dataset_iri) + "/")
    feature_collection_iri = URIRef(str(DS) + "det")

    # read the source data Shape files
    features = gpd.read_file(Path(__file__).parent.parent / "source" / "NTD_Register_Nat_shp" / "NTD_Register_Nat.shp")
    # print(features.columns)
    """
    ['TRIBID', 'NAME', 'FCNO', 'FCNAME', 'DETBODY', 'DETDATE', 'DETREGDATE',
           'DETMETHOD', 'DETTYPE', 'DETOUTCOME', 'APPEALDESC', 'JUDGE',
           'RNTBCNAME', 'NTHOLD', 'RELNTDA', 'AREASQKM', 'DATASOURCE', 'DATECURR',
           'SEADET', 'ZONELWM', 'ZONE3NM', 'ZONE12NM', 'ZONE24NM', 'ZONEEEZ',
           'NNTTSEQNO', 'SPTIALNOTE', 'LINK', 'JURIS', 'OVERLAP', 'DT_EXTRACT',
           'geometry'],
    """
    fc_no = URIRef(DS + "FederalCourtNo")
    g.add((fc_no, RDF.type, RDFS.Datatype))
    g.add((fc_no, RDFS.label, Literal("Federal Court Number")))

    print("Features...")
    for index, row in features.iterrows():
        print(row["TRIBID"])

        # Feature
        feature_iri = URIRef(DS + str(row["TRIBID"]).replace("/", "-"))
        g.add((feature_iri, RDF.type, GEO.Feature))
        g.add((feature_iri, DCTERMS.identifier, Literal(str(row["TRIBID"]).replace("/", "-"), datatype=XSD.token)))
        g.add((feature_iri, SDO.name, Literal(str(row["NAME"]).title())))
        g.add((feature_iri, SDO.identifier, Literal(str(row["FCNO"]), datatype=fc_no)))
        if str(row["AREASQKM"]) != "":
            g.add((feature_iri, GEO.hasMetricArea, Literal(float(row["AREASQKM"])*1000000, datatype=XSD.float)))

        if str(row["LINK"]) != "":
            g.add((feature_iri, RDFS.seeAlso, Literal(row["LINK"], datatype=XSD.anyURI)))

        # Geometry
        geom = BNode()
        g.add((geom, RDF.type, GEO.Geometry))
        # wkt = f'POINT ({row["LONGITUDE"]} {row["LATITUDE"]})'
        # g.add((geom, GEO.asWKT, Literal(wkt, datatype=GEO.wktLiteral)))
        geojson = json.dumps(shapely.geometry.mapping(row["geometry"]))
        g.add((geom, GEO.asGeoJSON, Literal(geojson, datatype=GEO.geoJSONLiteral)))

        g.add((feature_iri, GEO.hasGeometry, geom))

        # Feature Collection addition
        g.add((feature_collection_iri, RDFS.member, feature_iri))

        if index == 250:
            g.serialize(destination=f"../data/nntt-det-01.ttl", format="longturtle")
            g = Graph()
        if index == 300:
            g.serialize(destination=f"../data/nntt-det-02.ttl", format="longturtle")
            g = Graph()
        if index == 400:
            g.serialize(destination=f"../data/nntt-det-03.ttl", format="longturtle")
            g = Graph()
        if index == 500:
            g.serialize(destination=f"../data/nntt-det-04.ttl", format="longturtle")
            g = Graph()

    g.serialize(destination="../data/nntt-det-05.ttl", format="longturtle")
    print("complete processing")

