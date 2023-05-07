from lxml import etree
from rdflib import Graph, URIRef, Literal, BNode, Dataset
from rdflib.namespace import DCTERMS, GEO, RDF, RDFS, SDO, XSD

tree = etree.parse("source/ATNS_XML_05Apr22/Polygons.xml")

"""
<Polygons>
    <PolygonID>1</PolygonID>
    <PolygonID_ORG>1</PolygonID_ORG>
    <NAME> Kimberley</NAME>
    <STATE>WA</STATE>
    <MINX>119.9502052238</MINX>
    <MINY>-22.2074524067</MINY>
    <MAXX>128.9931546438</MAXX>
    <MAXY>-13.7313041997</MAXY>
    <Hidden>0</Hidden>
    <Updated>2012-01-24T04:46:12</Updated>
    <UpdatorID>718</UpdatorID>
    <Deleted>0</Deleted>
</Polygons>
"""
g = Graph(identifier="https://data.idnau.org/pid/atns")
stem = "https://data.idnau.org/pid/atns/feature/"

STATES = {
    "ACT": "https://linked.data.gov.au/dataset/asgsed3/STE/8",
    "NSW VIC": "https://linked.data.gov.au/dataset/asgsed3/STE/1,https://linked.data.gov.au/dataset/asgsed3/STE/2",
    "NSW": "https://linked.data.gov.au/dataset/asgsed3/STE/1",
    "NT": "https://linked.data.gov.au/dataset/asgsed3/STE/7",
    "QLD": "https://linked.data.gov.au/dataset/asgsed3/STE/3",
    "Qld": "https://linked.data.gov.au/dataset/asgsed3/STE/3",
    "SA/QLD": "https://linked.data.gov.au/dataset/asgsed3/STE/4,https://linked.data.gov.au/dataset/asgsed3/STE/3",
    "SA": "https://linked.data.gov.au/dataset/asgsed3/STE/4",
    "TAS": "https://linked.data.gov.au/dataset/asgsed3/STE/6",
    "Tas": "https://linked.data.gov.au/dataset/asgsed3/STE/6",
    "VIC": "https://linked.data.gov.au/dataset/asgsed3/STE/2",
    "Vic": "https://linked.data.gov.au/dataset/asgsed3/STE/2",
    "WA": "https://linked.data.gov.au/dataset/asgsed3/STE/5",
}

for poly in tree.findall(".//Polygons"):
    hidden = poly.find(".//Hidden").text.strip()
    if hidden == "0":
        i = poly.find(".//PolygonID").text.strip()
        try:
            name = poly.find(".//NAME").text.strip()
        except:
            name = None
        try:
            state = poly.find(".//STATE").text.strip()
        except:
            state = None
        minx = poly.find(".//MINX").text.strip()
        miny = poly.find(".//MINY").text.strip()
        maxx = poly.find(".//MAXX").text.strip()
        maxy = poly.find(".//MAXY").text.strip()
        try:
            updated = poly.find(".//Updated").text.strip()
        except:
            updated = None

        f = URIRef(stem + i.zfill(4))
        g.add((f, RDF.type, GEO.Feature))

        if name is not None:
            g.add((f, SDO.name, Literal(name)))

        if state is not None:
            s = STATES.get(state)
            if s is None:
                print(f"MISSING State {s}")
            else:
                if "," in s:
                    for ss in s.split(","):
                        g.add((f, GEO.sfOverlaps, URIRef(s)))
                else:
                    g.add((f, GEO.sfWithin, URIRef(s)))

        bn = BNode()
        g.add((bn, RDF.type, GEO.Geometry))
        # review online at https://tools.9revolution9.com/geo/wkt_geojson/
        g.add((bn, GEO.asWKT, Literal(f"POLYGON(({minx} {miny}, {maxx} {miny}, {maxx} {maxy}, {minx} {maxy}, {minx} {miny}))", datatype=GEO.wktLiteral)))
        g.add((f, GEO.hasGeometry, bn))
        if updated is not None:
            g.add((f, DCTERMS.modified, Literal(updated, datatype=XSD.dateTime)))

        # Feature Collection
        fc = URIRef("https://data.idnau.org/pid/atns/entity-areas")
        g.add((fc, RDFS.member, f))

g.serialize(destination="source/Polygons.ttl", format="longturtle")

g.parse("source/atns-metadata.ttl")
g.serialize(destination="atns.ttl", format="longturtle")

d = Dataset()
d.add_graph(g)
d.serialize(destination="atns.nq", format="nquads")
