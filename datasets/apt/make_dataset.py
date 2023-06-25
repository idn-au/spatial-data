from rdflib import Dataset, Graph

g = Graph(identifier="https://data.idnau.org/pid/apt")
# add each Feature Collection
g.parse("source/rdf/regions.ttl")
g.parse("source/rdf/places.ttl")

# add Dataset metadata
g.parse("source/rdf/dataset-metadata.ttl")

# write
d = Dataset()
d.add_graph(g)
d.serialize(destination="apt.nq", format="nquads")
