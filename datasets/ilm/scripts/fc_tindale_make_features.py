import json
from shapely.geometry import shape
from rdflib import URIRef, Literal, Namespace, BNode, Graph
from rdflib.namespace import DCTERMS, GEO, RDF, RDFS, XSD
import sys
sys.path.append("../../")
from utils import make_clean_id, bind_namespaces

g = Graph()
ILM = Namespace("https://data.idnau.org/pid/ILM/")
feature_collection = ILM.tindale

with open("../source/tindale.geojson") as f:
  features = json.load(f)["features"]

# NOTE: buffer(0) is a trick for fixing scenarios where polygons have overlapping coordinates
for f in features:
    tt = f["properties"]["TindaleTribe"]
    id = make_clean_id(tt)
    this_feature = URIRef("https://data.idnau.org/pid/ILM/feature/" + id)
    g.add((this_feature, RDF.type, GEO.Feature))
    g.add((this_feature, DCTERMS.identifier, Literal(id, datatype=XSD.token)))
    g.add((this_feature, RDFS.label, Literal(tt)))
    geom = BNode()
    g.add((this_feature, GEO.hasGeometry, geom))
    g.add((geom, RDF.type, GEO.Geometry))
    wkt = shape(f["geometry"]).buffer(0)
    g.add((geom, GEO.asWKT, Literal(wkt, datatype=GEO.wktLiteral)))
    comment_lines = []
    for k, v in f["properties"].items():
        if v != "":
            comment_lines.append(f"{k}: {v}")
    g.add((this_feature, RDFS.comment, Literal("\n".join(comment_lines))))

    g.add((feature_collection, RDFS.member, this_feature))

bind_namespaces(g)
g.serialize(destination="../source/fc-tindale.ttl", format="longturtle")
