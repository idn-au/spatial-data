import csv
from shapely.geometry import shape
from rdflib import URIRef, Literal, Namespace, BNode, Graph
from rdflib.namespace import DCTERMS, GEO, RDF, RDFS, XSD
import sys
sys.path.append("../../")
from utils import make_clean_id, bind_namespaces


g = Graph()
ILM = Namespace("https://w3id.org/idn/dataset/ILM/")
feature_collection = ILM.austlang

with open("../source/austlang_001.csv")as f:
    csvFile = csv.reader(f)
    next(csvFile, None)  # skip the headers
    for line in csvFile:
        lon = line[6].strip()
        lat = line[5].strip()
        if lon != "" and lat != "":
            id = line[0]
            this_feature = URIRef("https://w3id.org/idn/dataset/ILM/feature/" + id)
            g.add((this_feature, RDF.type, GEO.Feature))
            g.add((this_feature, DCTERMS.identifier, Literal(id, datatype=XSD.token)))
            g.add((this_feature, RDFS.label, Literal(line[1].strip())))
            geom = BNode()
            g.add((this_feature, GEO.hasGeometry, geom))
            g.add((geom, RDF.type, GEO.Geometry))
            wkt = f"POINT({lon} {lat})"
            g.add((geom, GEO.asWKT, Literal(wkt, datatype=GEO.wktLiteral)))
            g.add((this_feature, RDFS.seeAlso, URIRef(line[7])))

            g.add((feature_collection, RDFS.member, this_feature))

bind_namespaces(g)
g.serialize(destination="../source/fc-austlang.ttl", format="longturtle")

