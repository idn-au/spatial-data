from rdflib import Dataset, Graph

g = Graph(identifier="https://data.idnau.org/pid/capad2020")
# add each Feature Collection
g.parse("capad/source/features-mar.ttl")
g.parse("capad/source/features-ter.ttl")

# add Dataset metadata
g.parse("capad/source/capad-metadata.ttl")

# write
d = Dataset()
d.add_graph(g)
d.serialize(destination="capad2020.nq", format="nquads")
