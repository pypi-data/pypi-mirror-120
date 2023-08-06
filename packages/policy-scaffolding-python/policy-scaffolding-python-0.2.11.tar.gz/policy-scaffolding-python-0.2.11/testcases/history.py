import json
from typing import List
from fhir.resources.claim import Claim


def load_history(filename: str) -> Claim:
    """
    This function will load from file a Claim.  Note that the file passed into this function should be of type Claim
    and not of type InsightEngineTestCase.

    Parameters:
        filename (str): The name of the file to be loaded.

    Returns:
        Claim (Claim): Returns an object of type Claim.
    """
    return Claim.parse_file(filename)


def save_history(history: List[Claim], filename: str):
    """
    This function will save all claims within the history list to a file.

    Parameters:
        history (List[Claim]): A list of Claims.
        filename (str): The name of the file to be saved as.

    Returns:
        None
    """
    claims = []
    for claim in history:
        js = json.loads(claim.json())
        claims.append(js)
    with open(filename, 'w') as file:
        json.dump(claims, file, indent=2)
