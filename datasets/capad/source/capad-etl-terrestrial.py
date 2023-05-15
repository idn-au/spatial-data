from pathlib import Path
import geopandas as gpd
from shapely.geometry import shape
from rdflib import Graph, URIRef, BNode, Literal, Namespace
from rdflib.namespace import DCTERMS, GEO, PROV, RDF, RDFS, SDO, XSD

# https://data.gov.au/dataset/ds-environment-9984a9fd-3dd0-4e38-bfbd-7e788fa851a1/details?q=capad%202020
if __name__ == "__main__":
    # setup graph
    g = Graph()
    dataset_iri = URIRef("https://data.idnau.org/pid/capad2020")
    DS = Namespace(str(dataset_iri) + "/")
    feature_collection_iri_ipa = URIRef(str(DS) + "ipa")
    feature_collection_iri_npa = URIRef(str(DS) + "npa")

    g.add((feature_collection_iri_ipa, RDF.type, GEO.FeatureCollection))
    g.add((feature_collection_iri_npa, RDF.type, GEO.FeatureCollection))

    features = gpd.read_file(Path(__file__).parent / "source" / "CAPAD2020_terrestrial" / "CAPAD2020_terrestrial.shp")
    # print(features.columns)
    # ['OBJECTID', 'PA_ID', 'PA_PID', 'NAME', 'TYPE', 'TYPE_ABBR', 'IUCN',
    #        'NRS_PA', 'GAZ_AREA', 'GIS_AREA', 'GAZ_DATE', 'LATEST_GAZ', 'STATE',
    #        'AUTHORITY', 'DATASOURCE', 'GOVERNANCE', 'COMMENTS', 'ENVIRON',
    #        'OVERLAP', 'MGT_PLAN', 'RES_NUMBER', 'EPBC', 'LONGITUDE', 'LATITUDE',
    #        'SHAPE_Leng', 'SHAPE_Area', 'geometry']
    for index, row in features.iterrows():
        if str(row["TYPE_ABBR"]) in ["IPA", "NPA"]:
            feature_iri = URIRef(str(DS) + str(row["PA_PID"]))
            g.add((feature_iri, RDF.type, GEO.Feature))
            g.add((feature_iri, RDFS.label, Literal(str(row["NAME"]).title())))

            if row["TYPE_ABBR"] == "IPA":
                g.add((feature_collection_iri_ipa, RDFS.member, feature_iri))
            elif row["TYPE_ABBR"] == "NPA":
                g.add((feature_collection_iri_npa, RDFS.member, feature_iri))

            g.add((feature_iri, GEO.hasMetricArea, Literal(float(row["GIS_AREA"]) * 10000, datatype=XSD.float)))

            STATES = {
                "ACT": "https://linked.data.gov.au/dataset/asgsed3/STE/8",
                "NSW": "https://linked.data.gov.au/dataset/asgsed3/STE/1",
                "NT": "https://linked.data.gov.au/dataset/asgsed3/STE/7",
                "OT": "https://linked.data.gov.au/dataset/asgsed3/STE/9",
                "Z": "https://linked.data.gov.au/dataset/asgsed3/STE/Z",
                "QLD": "https://linked.data.gov.au/dataset/asgsed3/STE/3",
                "SA": "https://linked.data.gov.au/dataset/asgsed3/STE/4",
                "TAS": "https://linked.data.gov.au/dataset/asgsed3/STE/6",
                "VIC": "https://linked.data.gov.au/dataset/asgsed3/STE/2",
                "WA": "https://linked.data.gov.au/dataset/asgsed3/STE/5",

                "EXT": "https://linked.data.gov.au/dataset/asgsed3/STE/9",
                "JBT": "https://linked.data.gov.au/dataset/asgsed3/STE/8",  # Jervis Bay Territory
            }

            desc = """"""

            IUCNS = {
                "Ia": "Strict Nature Reserve",
                "Ib": "Wilderness Area",
                "II": "National Park",
                "III": "Natural Monument or Feature",
                "IV": "Habitat/Species Management Area",
                "V": "Protected Landscape/Seascape",
                "VI": "Protected area with sustainable use of natural resources",
                "NR": "Not Reported",
                "NA": "Not Applicable",
                "NAS": "Not Assigned",
            }
            desc += f"IUCN protected area management category: {IUCNS[row['IUCN']]}\n\n"

            AUTHORITIES = {
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
                "BRC_TAS": "Burnie Council - Tasmania",
                "CCC_TAS": "Clarence City Council – Tasmania",
                "DCC_TAS": "Devonport City Council - Tasmania",
                "DAWE": "Australian Government, Department of Climate Change, Energy, the Environment and Water",
                "DRC_TAS": "Dorset Council - Tasmania",
                "EAC_QLD": "Ewamian Aboriginal Corporation",
                "EL_NSW": "Enduring Landscapes Inc",
                "FC_NSW": "Forestry Corporation of NSW",
                "FUA": "Federation University Australia",
                "GCC_NSW": "Gosford City Council – New South Wales",
                "GCC_TAS": "Glenorchy City Council - Tasmania",
                "HCR_CMA": "Hunter Central Rivers Catchment Management Authority",
                "ILC": "Indigenous Land Corporation",
                "IMG": "Indigenous Management Group",
                "KNC_TAS": "Kingborough Council - Tasmania",
                "KRGC_NSW": "Ku-ring-gai Council – New South Wales",
                "LCC_TAS": "Launceston City Council - Tasmania",
                "LILC": "Local Indigenous Land Council",
                "MINCA_QLD": "Magnetic Island Nature Care Association",
                "NF_SA": "Nature Foundation South Australia Inc",
                "NMC_TAS": "Northern Midlands Council - Tasmania",
                "NSC_QLD": "Noosa Shire Council - Queensland",
                "NSW_OEH": "NSW Office of Environment and Heritage",
                "NT_PWCNT": "Parks and Wildlife Commission of the NT",
                "NTWA": "National Trust of Western Australia",
                "QLD_DES": "Queensland Department of Environment and Science",
                "SA_DEW": "South Australian Department of Environment and Water",
                "SA_FRST": "Forestry South Australia",
                "SET": "South Endeavour Trust",
                "SHFT": "Sydney Harbour Federation Trust",
                "SMC_TAS": "Southern Midlands Council - Tasmania",
                "TAS_DPIPWE": "Tasmanian Department of Primary Industries, Parks, Water and Environment",
                "TAS_HYDRO": "Hydro Tasmania",
                "TAS_PAHSMA": "Port Arthur Historic Site Management Authority - Tasmania",
                "TAS_PRIV": "Private (miscellaneous) – Tasmania",
                "TAS_VAR": "Various managing authorities - Tasmania",
                "TAS_WATER": "TasWater",
                "TAS_WPMT": "Wellington Park Management Trust - Tasmania",
                "TFN_QLD": "Queensland Trust for Nature",
                "TFN_VIC": "Trust for Nature Victoria",
                "TLC": "Tasmanian Land Conservancy Inc",
                "TSRA": "Torres Strait Regional Authority",
                "VIC_DELWP": "Victorian Department of Environment, Land, Water and Planning",
                "WA_DBCA": "Western Australian Department of Biodiversity, Conservation and Attractions",
                "WAC": "Winangakirri Aboriginal Corporation",
            }
            desc += f"Authority: {AUTHORITIES[row['AUTHORITY']]}\n\n"

            GOVERNANCES = {
                "C": "Community - Community conserved areas where indigenous peoples or local communities (settled or mobile) hold decision-making authority, responsibility and accountability.",
                "G": "Government - Protected areas with decision-making authority, responsibility and accountability in the hands of national, state or local government.",
                "J": "Joint - Jointly managed protected areas where several social actors from different governance types share decision-making authority, responsibility and accountability. Joint management arrangements are recognised by a management board, agreement (e.g. ILUA) or other formal arrangement.",
                "P": "Private - Private protected areas where land and resource owners hold decision-making authority, responsibility and accountability.",
            }
            desc += f"Governance: {GOVERNANCES[row['GOVERNANCE']]}"

            g.add((feature_iri, SDO.description, Literal(desc)))

            role_iri = URIRef("http://def.isotc211.org/iso19115/-1/2018/CitationAndResponsiblePartyInformation/code/CI_RoleCode/contributor")
            agent_iri = URIRef("https://linked.data.gov.au/org/capad-" + str(row["AUTHORITY"]))
            wat = BNode()
            g.add((feature_iri, PROV.wasAttributedTo, wat))
            g.add((wat, PROV.hadRole, role_iri))
            g.add((wat, PROV.agent, agent_iri))

            DATASOURCES = {
                "AAD": "Australian Antarctic Division",
                "ACT_EPSSD": "ACT Environment, Planning and Sustainable Development Directorate",
                "AWC": "Australian Wildlife Conservancy",
                "BHA": "Bush Heritage Australia",
                "BHA_NTWA": "Bush Heritage Australia and National Trust of Western Australia",
                "DAWE": "Australian Government, Department of Climate Change, Energy, the Environment and Water",
                "DOEE_NRSP": "Australian Government, Department of Climate Change, Energy, the Environment and Water - National Reserve System Program",
                "FC_NSW": "Forestry Corporation of NSW",
                "LHI_Board": "Lord Howe Island Board",
                "NF_SA": "Nature Foundation SA Inc",
                "NSW_OEH": "NSW Office of Environment and Heritage",
                "NT_PWCNT": "Parks and Wildlife Commission of the NT",
                "NTWA": "National Trust of Western Australia",
                "QLD_DES": "Queensland Department of Environment and Science",
                "SA_DEW": "South Australian Department for Environment and Water",
                "SA_FRST": "Forestry South Australia",
                "TAS_DPIPWE": "Tasmanian Department of Primary Industries, Parks, Water and Environment",
                "TFN_QLD": "Queensland Trust for Nature",
                "TFN_VIC": "Trust for Nature Victoria",
                "TSRA": "Torres Strait Regional Authority",
                "VIC_DELWP": "Victorian Department of Environment, Land, Water and Planning",
                "WA_DBCA": "Western Australian Department of Biodiversity, Conservation and Attractions",
            }

            g.add((feature_iri, DCTERMS.provenance, Literal(row["DATASOURCE"])))

            # Geometry
            geom = BNode()
            g.add((feature_iri, GEO.hasGeometry, geom))
            g.add((geom, RDF.type, GEO.Geometry))
            wkt = shape(row["geometry"]).buffer(0)
            g.add((geom, GEO.asWKT, Literal(wkt, datatype=GEO.wktLiteral)))

    g.serialize(destination="source/features-ter.ttl", format="longturtle")
