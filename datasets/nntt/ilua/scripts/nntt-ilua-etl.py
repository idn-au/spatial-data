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
    feature_collection_iri = URIRef(str(DS) + "ilua")

    # read the source data Shape files
    features = gpd.read_file(Path(__file__).parent.parent / "source" / "ILUA_Registered_Notified_Nat.shp")
    """
    ['TRIBID', 'NAME', 'AGSTATUS', 'DATELODGED', 'DATENOTIF', 'NOTIFCLOSE',
       'DATEREGD', 'SUBJMATTER', 'AGTYPE', 'CONSENTFA', 'RTN', 'SURRAREAS',
       'VALIDATEFA', 'INTERMACTS', 'AGAUTH', 'APPLICANT', 'REP', 'TIMEFSTART',
       'TIMEFEND', 'AREASQKM', 'DATASOURCE', 'DATECURR', 'SEAILUA', 'ZONELWM',
       'ZONE3NM', 'ZONE12NM', 'ZONE24NM', 'ZONEEEZ', 'NNTTSEQNO', 'SPTIALNOTE',
       'GTREF', 'DATEASSIST', 'JURIS', 'OVERLAP', 'DT_EXTRACT', 'geometry'],
    """

    print("Features...")
    for index, row in features.iterrows():
        print(row["TRIBID"])

        # Feature
        feature_iri = URIRef(str(DS) + str(row["TRIBID"]).replace("/", "-"))
        g.add((feature_iri, RDF.type, GEO.Feature))
        g.add((feature_iri, RDFS.label, Literal(str(row["NAME"]).title())))
        if str(row["AREASQKM"]) != "":
            g.add((feature_iri, GEO.hasMetricArea, Literal(float(row["AREASQKM"])*1000000, datatype=XSD.float)))

        # Geometry
        geom = BNode()
        g.add((geom, RDF.type, GEO.Geometry))
        g.add((geom, GEO.asWKT, Literal(row["geometry"], datatype=GEO.wktLiteral)))
        geojson = json.dumps(shapely.geometry.mapping(row["geometry"]))

        g.add((feature_iri, GEO.hasGeometry, geom))

        # Feature Collection addition
        g.add((feature_collection_iri, RDFS.member, feature_iri))

        if index == 250:
            g.serialize(destination=f"../data/nntt-ilua-01.ttl", format="longturtle")
            g = Graph()
        if index == 500:
            g.serialize(destination=f"../data/nntt-ilua-02.ttl", format="longturtle")
            g = Graph()
        if index == 750:
            g.serialize(destination=f"../data/nntt-ilua-03.ttl", format="longturtle")
            g = Graph()
        if index == 1000:
            g.serialize(destination=f"../data/nntt-ilua-04.ttl", format="longturtle")
            g = Graph()
        if index == 1200:
            g.serialize(destination=f"../data/nntt-ilua-05.ttl", format="longturtle")
            g = Graph()
        if index == 1300:
            g.serialize(destination=f"../data/nntt-ilua-06.ttl", format="longturtle")
            g = Graph()

    g.serialize(destination="../data/nntt-ilua-07.ttl", format="longturtle")

    print("complete processing")

    # conforms, results_graph, results_text = validate(resultant_data_file, shacl_graph="../../../validator.ttl")
    # if not conforms:
    #     print(results_text)
    # else:
    #     print("valid")
