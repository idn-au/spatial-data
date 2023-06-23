# This tests the IPA Dedicated datset (https://www.dcceew.gov.au/environment/land/indigenous-protected-areas)
# to determine whether it's a true subset of the CAPAD terrestrial & marine datasets (https://www.dcceew.gov.au/environment/land/nrs/science/capad)

from pathlib import Path
import geopandas as gpd


if __name__ == "__main__":
    ipa_dedicated = gpd.read_file(Path(__file__).parent / "ipa_dedicated_public" / "ipa_dedicated.shp")
    # print(features.columns)
    """
    ['OBJECTID', 'NAME', 'TYPE', 'STATE', 'STATUS', 'GAZ_AREA', 'IUCN_CODE',
    'AUTHORITY', 'GAZ_DATE', 'LATEST_GAZ', 'ENVIRON', 'SOURCE', 'COMMENTS',
    'CP_APPROVE', 'GIS_AREA', 'LONGITUDE', 'LATITUDE', 'IPA_ID_SOR',
    'IPA_ID', 'X', 'Y', 'SHAPE_Leng', 'SHAPE_Area', 'geometry']
    """
    ipa_dedicated_names = ipa_dedicated["NAME"].unique()
    ipa_dedicated_names.sort()

    marine_features = gpd.read_file(Path(__file__).parent / "CAPAD2020_marine" / "CAPAD2020_marine.shp")
    marine_ipas = marine_features[marine_features["TYPE_ABBR"] == "IPA"]
    marine_ipas_names = marine_ipas["NAME"].unique()
    marine_ipas_names.sort()

    terrestrial_features = gpd.read_file(Path(__file__).parent / "CAPAD2020_terrestrial" / "CAPAD2020_terrestrial.shp")
    terrestrial_ipas = terrestrial_features[terrestrial_features["TYPE_ABBR"] == "IPA"]
    terrestrial_ipas_names = terrestrial_ipas["NAME"].unique()
    terrestrial_ipas_names.sort()

    print(f"ipa_dedicated_names: {len(ipa_dedicated_names)}")
    print(f"marine_ipas_names: {len(marine_ipas_names)}")
    print(f"terrestrial_ipas_names: {len(terrestrial_ipas_names)}")

    capad_ipas_names = set(marine_ipas_names).union(terrestrial_ipas_names)
    print(len(set(ipa_dedicated_names).difference(capad_ipas_names)))

    with open("labels.csv", "w") as f:
        for i in range(84):
            indep = ipa_dedicated_names[i] if i < len(ipa_dedicated_names) else ''
            terr = terrestrial_ipas_names[i] if i < len(terrestrial_ipas_names) else ''
            mar = marine_ipas_names[i] if i < len(marine_ipas_names) else ''
            f.write(f"{indep}, {terr}, {mar}\n")
