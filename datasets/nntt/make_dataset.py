from rdflib import Dataset, Graph

g = Graph(identifier="https://data.idnau.org/pid/nntt")
# add each Feature Collection
g.parse("det/nntt-det.ttl")
g.parse("ilua/nntt-ilua.ttl")

# add Dataset metadata
g.parse("source/nntt-metadata.ttl")

# write
d = Dataset()
d.add_graph(g)
d.serialize(destination="nntt.nq", format="nquads")
