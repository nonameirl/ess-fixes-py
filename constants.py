# constants.py
from pathlib import Path



EXTRACT_DIR = Path("extracted")
ZIP_DIR = Path("zips")
COMPLETE_DIR = Path("completed")
PDF_DIR = Path("2D")
OFFICE_FILE = "Offices.txt"
PRECINCT_FILE = "Precincts.txt"
CANDIDATE_FILE = "Candidates.txt"
BOD_DIR = Path("BallotOnDemand_Export")
IMPORT_DIR = Path("Import")
BOD_ZIP = Path("BallotOnDemand_Export.ezip")
README_FILE = "Readme.txt"


class Location:
    def __init__(self, county, state):
        self.state = state
        self.county = county

