from pathlib import Path
from rdflib import Graph, Dataset, URIRef, BNode, Literal, Namespace
from rdflib.namespace import DCTERMS, GEO, RDF, RDFS, SDO, XSD
import pandas as pd
from pyshacl import validate


if __name__ == "__main__":
    # setup graph
    g = Graph(identifier="https://data.idnau.org/pid/agil")
    dataset_iri = URIRef("https://data.idnau.org/pid/agil")
    DS = Namespace(str(dataset_iri) + "/")
    feature_collection_iri = URIRef(DS + "point-locations")

    # read the source data Excel file "LOCATIONS" worksheet into a PANDAS dataframe
    df = pd.read_excel(
        Path(__file__).parent / "source" / "agil20190208.xlsx",
        sheet_name="LOCATIONS"
    )

    print("Features...")
    for index, row in df.iterrows():
        print(row["LCODE"])
        # Feature
        feature_iri = URIRef(DS + str(row["LCODE"]))
        g.add((feature_iri, RDF.type, GEO.Feature))

        # Geometry
        geom = BNode()
        g.add((geom, RDF.type, GEO.Geometry))
        wkt = f'POINT ({row["LONGITUDE"]} {row["LATITUDE"]})'
        g.add((geom, GEO.asWKT, Literal(wkt, datatype=GEO.wktLiteral)))
        # geojson = f'{{"type": "Point", "coordinates": [{row["LONGITUDE"]}, {row["LATITUDE"]}]}}'
        # g.add((geom, GEO.asGeoJSON, Literal(geojson, datatype=GEO.geoJSONLiteral)))

        g.add((feature_iri, GEO.hasGeometry, geom))

        # Feature Collection addition
        g.add((feature_collection_iri, RDFS.member, feature_iri))

    # read the source data Excel file "NAMES" worksheet into a PANDAS dataframe
    df = pd.read_excel(
        Path(__file__).parent / "source" / "agil20190208.xlsx",
        sheet_name="NAMES"
    )

    print("Names...")
    for index, row in df.iterrows():
        print(row["LCODE"])
        feature_iri = URIRef(DS + str(row["LCODE"]))
        if str(row["NFLAG"]) == "P":
            g.add((feature_iri, SDO.name, Literal(str(row["NAME"]).title())))
        else:  # == "A"
            g.add((feature_iri, SDO.alternateName, Literal(str(row["NAME"]).title())))

    # merge with metadata
    g.parse(Path(__file__).parent / "source" / "agil-metadata.ttl")

    # save to file
    resultant_data_file = Path(__file__).parent / "agil.nq"
    d = Dataset()
    d.add_graph(g)
    d.serialize(
        destination=resultant_data_file,
        format="nquads"
    )
    # d.serialize(
    #     destination=Path(__file__).parent / "agil.trig",
    #     format="trig"
    # )
    print("complete processing")

