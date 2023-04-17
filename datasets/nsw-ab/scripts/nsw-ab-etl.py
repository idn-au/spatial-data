import json
from pathlib import Path
from rdflib import Graph, URIRef, BNode, Literal, Namespace
from rdflib.namespace import DCAT, GEO, RDF, RDFS
from shapely.geometry import shape

data = json.load(open(Path(__file__).parent.parent / "source" / "LocalAboriginalLandCouncil_EPSG4326.json"))

g = Graph()
DS = Namespace("https://data.idnau.org/pid/NSW-AB/")

for i, feature in enumerate(data["LocalAboriginalLandCouncil"]["features"]):
    # Regional Council
    # Feature
    rc_iri = URIRef(DS + "feature/" + str(feature["properties"]["regionalcouncilname"]).title().replace(" ", "-"))
    g.add((rc_iri, RDF.type, GEO.Feature))
    g.add((rc_iri, RDFS.label, Literal(str(feature["properties"]["regionalcouncilname"]).title())))
    # Feature Collection addition
    g.add((URIRef(DS + "ralc"), RDFS.member, rc_iri))

    # Local Council
    # Feature
    feature_iri = URIRef(DS + "feature/" + str(feature["properties"]["rid"]))
    g.add((feature_iri, RDF.type, GEO.Feature))
    g.add((feature_iri, RDFS.label, Literal(str(feature["properties"]["localcouncilname"]).title())))
    g.add((feature_iri, DCAT.theme, URIRef("https://data.idnau.org/pid/vocab/urbanity/" + str(feature["properties"]["urbanity"]))))

    # link local council to regional council
    g.add((feature_iri, GEO.sfWithin, rc_iri))
    # Feature Collection addition
    g.add((URIRef(DS + "lalc"), RDFS.member, feature_iri))

    # Geometry
    geom = BNode()
    g.add((geom, RDF.type, GEO.Geometry))
    g.add((geom, GEO.asWKT, Literal(shape(feature["geometry"]).wkt, datatype=GEO.wktLiteral)))

    g.add((feature_iri, GEO.hasGeometry, geom))

    if i == 50:
        g.serialize(destination=f"../data/nsw-ab-01.ttl")
        g = Graph()
    if i == 100:
        g.serialize(destination=f"../data/nsw-ab-02.ttl")
        g = Graph()

g.serialize(destination="../data/nsw-ab-03.ttl")
