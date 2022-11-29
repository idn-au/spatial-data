from rdflib import Graph

g = Graph()
# add each Feature Collection
g.parse("../source/fc-tindale.ttl")
g.parse("../source/fc-austlang.ttl")

# add Dataset metadata
g.parse("../ilm-metadata-dataset.ttl")

# add Resource metadata
g.parse("../ilm-metadata-resource.ttl")

# write
g.serialize(destination="../data/ilm.ttl", format="longturtle")
