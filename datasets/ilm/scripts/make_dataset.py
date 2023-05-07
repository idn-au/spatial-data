from rdflib import Dataset, Graph

g = Graph(identifier="https://data.idnau.org/pid/ilm")
# add each Feature Collection
# g.parse("../source/fc-tindale.ttl")
g.parse("../source/fc-austlang.ttl")

# add Dataset metadata
g.parse("../source/ilm-metadata.ttl")

# write
d = Dataset()
d.add_graph(g)
d.serialize(destination="../ilm.nq", format="nquads")
