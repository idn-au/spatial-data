import os

from pathlib import Path

from urllib import request


def validator():
    """
    NB this uses Jena shacl validator, not pyshacl, as it is faster.
    as such Jena must be installed.
    :return:
    """

    validator_file = "https://raw.githubusercontent.com/GeoscienceAustralia/fsdf-supermodel/main/backbone-model-profile/validator.ttl"
    r = request.Request(validator_file)
    resp = request.urlopen(r)
    with open('latest_validator.ttl', 'wb') as f:
        f.write(resp.read())
    for file in Path('../datasets').glob('**/data/**/*'):
        if file.is_file():
            print(f"Validating {file.name} using {validator_file}")
            os.system(f"shacl v --shapes latest_validator.ttl --data {str(file)} > reports/{file.stem}.ttl")



if __name__ == "__main__":
    validator()