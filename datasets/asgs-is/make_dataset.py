from rdflib import Dataset, Graph
import os

g = Graph(identifier="https://data.idnau.org/pid/asgs-is")
d = Dataset()
d.add_graph(g)
d.serialize(destination="source/asgs-is.nq", format="nquads")

os.system(f"cat source/*.nq > asgs-is.nq")
