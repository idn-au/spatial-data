import os

from pathlib import Path

from urllib import request


def validator():
    """
    NB this uses Jena shacl validator, not pyshacl, as it is faster.
    as such Jena must be installed.

    e.g.
        export JENA_HOME=/Users/nick/Work/apache-jena-4.5.0
        export PATH=$PATH:$JENA_HOME/bin

    :return:
    """

    if not Path("latest_validator.ttl").is_file():
        validator_file = "https://raw.githubusercontent.com/GeoscienceAustralia/fsdf-supermodel/main/backbone-model-profile/validator.ttl"
        r = request.Request(validator_file)
        resp = request.urlopen(r)
        with open('latest_validator.ttl', 'wb') as f:
            f.write(resp.read())

    datasets = [
        # (Path(__file__).parent.parent / "datasets/agil/agil.nq", "https://data.idnau.org/pid/agil"),
        # (Path(__file__).parent.parent / "datasets/asgs-is/asgs-is.nq", "https://data.idnau.org/pid/asgs-is"),
        # (Path(__file__).parent.parent / "datasets/ilm/ilm.nq", "https://data.idnau.org/pid/ilm"),
        # (Path(__file__).parent.parent / "datasets/nntt/nntt.nq", "https://data.idnau.org/pid/nntt"),
        # (Path(__file__).parent.parent / "datasets/nsw-ab/nsw-ab.nq", "https://data.idnau.org/pid/nsw-ab"),
        (Path(__file__).parent.parent / "datasets/apt/apt.nq", "https://data.idnau.org/pid/apt"),
    ]
    # produce n-triples
    for dataset, iri in datasets:
        print(f"Converting {dataset}")
        os.system(f"sed 's#<{iri}> \.$#.#g' {dataset} > {str(dataset).replace('.nq', '.nt')}")

    # # validate NT
    # for dataset, iri in datasets:
    #     print(f"Validating {dataset.name}")
    #     os.system("source ~/jena-source.sh")
    #     os.system(f"shacl v --shapes latest_validator.ttl --data {str(dataset).replace('.nq', '.nt')} > reports/{dataset.stem}.ttl")


if __name__ == "__main__":
    validator()
