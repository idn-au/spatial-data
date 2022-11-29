import re
from rdflib import Graph, Namespace
from rdflib.namespace import DCTERMS, GEO, RDF, RDFS, SDO, XSD


def make_clean_id(s) -> str:
    return re.subn("[(),\s]", "-", str(s).lower())[0].replace("--", "-").replace("--", "-").strip("-")


def bind_namespaces(g: Graph):
    g.bind("geo", GEO)
    g.bind("dcterms", DCTERMS)
    g.bind("feat", Namespace("https://w3id.org/idn/dataset/ILM/feature/"))
