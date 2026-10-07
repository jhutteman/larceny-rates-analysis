"""
Build data/crimedata.csv from the UCI "Communities and Crime Unnormalized" download.

The raw UCI file (CommViolPredUnnormalizedData.txt) has no header row, and the
column names UCI shows on its website today differ from the original names this
project uses (e.g. "pctBlack" vs "racepctblack"). This script attaches the
original 147 column names so the analysis notebook can read the data directly.

Usage (from the repository root):
    python scripts/make_dataset.py path/to/communities+and+crime+unnormalized.zip

You can pass either the downloaded .zip or the extracted .txt file.

Data source:
    Redmond, M. (2011). Communities and Crime Unnormalized [Dataset].
    UCI Machine Learning Repository.
    https://archive.ics.uci.edu/dataset/211/communities+and+crime+unnormalized
"""

import io
import sys
import zipfile
from pathlib import Path

import pandas as pd

RAW_FILENAME = "CommViolPredUnnormalizedData.txt"
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "crimedata.csv"

# Original attribute names, in file order (147 columns).
COLUMNS = [
    "communityname", "state", "countyCode", "communityCode", "fold",
    "population", "householdsize", "racepctblack", "racePctWhite",
    "racePctAsian", "racePctHisp", "agePct12t21", "agePct12t29", "agePct16t24",
    "agePct65up", "numbUrban", "pctUrban", "medIncome", "pctWWage",
    "pctWFarmSelf", "pctWInvInc", "pctWSocSec", "pctWPubAsst", "pctWRetire",
    "medFamInc", "perCapInc", "whitePerCap", "blackPerCap", "indianPerCap",
    "AsianPerCap", "OtherPerCap", "HispPerCap", "NumUnderPov", "PctPopUnderPov",
    "PctLess9thGrade", "PctNotHSGrad", "PctBSorMore", "PctUnemployed",
    "PctEmploy", "PctEmplManu", "PctEmplProfServ", "PctOccupManu",
    "PctOccupMgmtProf", "MalePctDivorce", "MalePctNevMarr", "FemalePctDiv",
    "TotalPctDiv", "PersPerFam", "PctFam2Par", "PctKids2Par",
    "PctYoungKids2Par", "PctTeen2Par", "PctWorkMomYoungKids", "PctWorkMom",
    "NumKidsBornNeverMar", "PctKidsBornNeverMar", "NumImmig", "PctImmigRecent",
    "PctImmigRec5", "PctImmigRec8", "PctImmigRec10", "PctRecentImmig",
    "PctRecImmig5", "PctRecImmig8", "PctRecImmig10", "PctSpeakEnglOnly",
    "PctNotSpeakEnglWell", "PctLargHouseFam", "PctLargHouseOccup",
    "PersPerOccupHous", "PersPerOwnOccHous", "PersPerRentOccHous",
    "PctPersOwnOccup", "PctPersDenseHous", "PctHousLess3BR", "MedNumBR",
    "HousVacant", "PctHousOccup", "PctHousOwnOcc", "PctVacantBoarded",
    "PctVacMore6Mos", "MedYrHousBuilt", "PctHousNoPhone", "PctWOFullPlumb",
    "OwnOccLowQuart", "OwnOccMedVal", "OwnOccHiQuart", "OwnOccQrange",
    "RentLowQ", "RentMedian", "RentHighQ", "RentQrange", "MedRent",
    "MedRentPctHousInc", "MedOwnCostPctInc", "MedOwnCostPctIncNoMtg",
    "NumInShelters", "NumStreet", "PctForeignBorn", "PctBornSameState",
    "PctSameHouse85", "PctSameCity85", "PctSameState85", "LemasSwornFT",
    "LemasSwFTPerPop", "LemasSwFTFieldOps", "LemasSwFTFieldPerPop",
    "LemasTotalReq", "LemasTotReqPerPop", "PolicReqPerOffic", "PolicPerPop",
    "RacialMatchCommPol", "PctPolicWhite", "PctPolicBlack", "PctPolicHisp",
    "PctPolicAsian", "PctPolicMinor", "OfficAssgnDrugUnits",
    "NumKindsDrugsSeiz", "PolicAveOTWorked", "LandArea", "PopDens",
    "PctUsePubTrans", "PolicCars", "PolicOperBudg", "LemasPctPolicOnPatr",
    "LemasGangUnitDeploy", "LemasPctOfficDrugUn", "PolicBudgPerPop",
    "murders", "murdPerPop", "rapes", "rapesPerPop", "robberies",
    "robbbPerPop", "assaults", "assaultPerPop", "burglaries", "burglPerPop",
    "larcenies", "larcPerPop", "autoTheft", "autoTheftPerPop", "arsons",
    "arsonsPerPop", "ViolentCrimesPerPop", "nonViolPerPop",
]
assert len(COLUMNS) == 147


def read_raw(path: Path) -> pd.DataFrame:
    """Read the header-less UCI file from a .zip or a .txt."""
    if path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path) as zf:
            matches = [n for n in zf.namelist() if n.endswith(RAW_FILENAME)]
            if not matches:
                sys.exit(f"Couldn't find {RAW_FILENAME} inside {path}")
            text = zf.read(matches[0]).decode("latin1")
        source = io.StringIO(text)
    else:
        source = path

    # Missing values are written as "?" in the raw file. They're kept as "?"
    # here so the notebook reproduces the original analysis exactly.
    return pd.read_csv(source, header=None, names=COLUMNS, dtype=str,
                       keep_default_na=False, encoding="latin1")


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)

    raw_path = Path(sys.argv[1]).expanduser()
    if not raw_path.exists():
        sys.exit(f"File not found: {raw_path}")

    df = read_raw(raw_path)
    if df.shape != (2215, 147):
        print(f"Warning: expected 2215 rows x 147 columns, got {df.shape}.")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved {df.shape[0]} rows x {df.shape[1]} columns to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
