from rdflib import Graph, URIRef, BNode, Literal, Namespace
from rdflib.namespace import DCTERMS, GEO, RDF, RDFS, SDO, XSD


agents = {
    "AAD": "Australian Antarctic Division",
    "ACT_EPSDD": "Environment, Planning and Sustainable Development Directorate",
    "AWC": "Australian Wildlife Conservancy",
    "AWC_BA": "Australian Wildlife Conservancy and Birdlife Australia",
    "AWC_DAM": "Australian Wildlife Conservancy and Dambimangari People",
    "AWC_DD": "Australian Wildlife Conservancy and Department of Defence",
    "AWC_TLLFW": "Australian Wildlife Conservancy and Tony and Lisette Lewis Foundation WildlifeLink",
    "AWC_YC": "Australian Wildlife Conservancy and Yulmbu Community",
    "BHA": "Bush Heritage Australia",
    "BHA_NTWA": "Bush Heritage Australia and National Trust of Western Australia",
    "BRC_TAS": "Burnie Council",
    "CCC_TAS": "Clarence City Council – Tasmania",
    "DCC_TAS": "Devonport City Council",
    "DAWE": "Australian Government, Department of Climate Change, Energy, the Environment and Water",
    "DRC_TAS": "Dorset Council",
    "EAC_QLD": "Ewamian Aboriginal Corporation",
    "EL_NSW": "Enduring Landscapes Inc",
    "FC_NSW": "Forestry Corporation of NSW",
    "FUA": "Federation University Australia",
    "GCC_NSW": "Gosford City Council – New South Wales",
    "GCC_TAS": "Glenorchy City Council",
    "HCR_CMA": "Hunter Central Rivers Catchment Management Authority",
    "ILC": "Indigenous Land Corporation",
    "IMG": "Indigenous Management Group",
    "KNC_TAS": "Kingborough Council",
    "KRGC_NSW": "Ku-ring-gai Council – New South Wales",
    "LCC_TAS": "Launceston City Council",
    "LILC": "Local Indigenous Land Council",
    "MINCA_QLD": "Magnetic Island Nature Care Association",
    "NF_SA": "Nature Foundation South Australia Inc",
    "NMC_TAS": "Northern Midlands Council",
    "NSC_QLD": "Noosa Shire Council - Queensland",
    "NSW_OEH": "NSW Office of Environment and Heritage",
    "NT_PWCNT": "Parks and Wildlife Commission of the NT",
    "NTWA": "National Trust of Western Australia",
    "QLD_DES": "Queensland Department of Environment and Science",
    "SA_DEW": "South Australian Department of Environment and Water",
    "SA_FRST": "Forestry South Australia",
    "SET": "South Endeavour Trust",
    "SHFT": "Sydney Harbour Federation Trust",
    "SMC_TAS": "Southern Midlands Council",
    "TAS_DPIPWE": "Tasmanian Department of Primary Industries, Parks, Water and Environment",
    "TAS_HYDRO": "Hydro Tasmania",
    "TAS_PAHSMA": "Port Arthur Historic Site Management Authority",
    "TAS_PRIV": "Private (miscellaneous) – Tasmania",
    "TAS_VAR": "Various managing authorities",
    "TAS_WATER": "TasWater",
    "TAS_WPMT": "Wellington Park Management Trust",
    "TFN_QLD": "Queensland Trust for Nature",
    "TFN_VIC": "Trust for Nature Victoria",
    "TLC": "Tasmanian Land Conservancy Inc",
    "TSRA": "Torres Strait Regional Authority",
    "VIC_DELWP": "Victorian Department of Environment, Land, Water and Planning",
    "WA_DBCA": "Western Australian Department of Biodiversity, Conservation and Attractions",
    "WAC": "Winangakirri Aboriginal Corporation",
}

g = Graph()
for k, v in agents.items():
    agent_iri = URIRef("https://linked.data.gov.au/org/capad-" + k)
    g.add((agent_iri, RDF.type, SDO.organization))
    g.add((agent_iri, SDO.name, Literal(v)))

g.serialize(destination="capad-authorities.ttl", format="longturtle")
