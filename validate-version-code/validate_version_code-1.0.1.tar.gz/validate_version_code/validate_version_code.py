import re

def validate_version_code(version_code:str)->bool:
    """Return a boolean representing if given version code is valid.
        version_code:str, the version code to validate.
    """
    return bool(re.compile(r"\d+\.\d+\.\d+").match(version_code))

def extract_version_code(path:str)->str:
    """Return the version code from given project."""
    with open("{path}/__version__.py".format(path=path), "r") as f:
        return re.compile(r"(\d+\.\d+\.\d+)").findall(f.read())[0]