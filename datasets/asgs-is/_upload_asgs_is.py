import httpx

r = httpx.post(
    "https://idn-fuseki.australiaeast.azurecontainer.io/agentsdb",
    params={"graph": "https://data.idnau.org/pid/spacecat/ASGS-IS-data"},
    content=open("asgs-is-metadata.ttl").read(),
    headers={"Content-Type": "text/turtle"},
    auth=("admin", "TKSHG38&PjCC%b!og$rfxc&2o2z53eEmJmVv"),
)
print(r.status_code)
