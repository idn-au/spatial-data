from pathlib import Path

import geopandas as gpd
from shapely.geometry import shape
from rdflib import Graph, URIRef, BNode, Literal, Namespace
from rdflib.namespace import DCTERMS, GEO, PROV, RDF, RDFS, SDO, XSD

if __name__ == "__main__":
    g = Graph()
    dataset_iri = URIRef("https://data.idnau.org/pid/nola")
    DS = Namespace(str(dataset_iri) + "/")
    EGO = Namespace("https://idn-au.github.io/ext-geom-ont/ego")
    EGOR = Namespace("https://w3id.org/idn/def/ego/role/")
    g.bind("ego", EGO)
    g.bind("egor", EGOR)
    g.bind("geo", GEO)
    features = gpd.read_file(Path(__file__).parent / "features/features.shp")
    grouped = features.groupby("featureId")
    for name, group in grouped:
        feature_iri = URIRef(str(DS) + name)
        g.add((feature_iri, RDF.type, GEO.Feature))

        # Geometry
        for index, row in group.iterrows():
            qual_geom = BNode()
            g.add((qual_geom, RDF.type, EGO.QualifiedGeometry))
            g.add((feature_iri, EGO.hasQualifiedGeometry, qual_geom))
            geom = BNode()
            g.add((geom, RDF.type, GEO.Geometry))
            wkt = shape(row["geometry"]).buffer(0)
            g.add((geom, GEO.asWKT, Literal(wkt, datatype=GEO.wktLiteral)))
            g.add((qual_geom, EGO.hasGeometry, geom))
            g.add((qual_geom, EGO.hasGeometryRole, EGOR.BoundaryEstimate))
            g.add((qual_geom, EGO.hasEvidence, Literal(f"{row['confidence']} certainty boundary derived from hand drawn map")))
            g.add((qual_geom, EGO.hasConfidence, Literal(row["confidence"])))

    parent_dir = Path(__file__).parent
    g.serialize(destination=parent_dir / "features.ttl", format="longturtle")
