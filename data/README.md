# Data

All data used in the analysis is included in this folder.

| File | Description |
|---|---|
| `crimedata.csv` | Data used by the notebook. Created from the UCI download by `scripts/make_dataset.py`, which adds the column names. |
| `communities+and+crime+unnormalized.zip` | Original, unmodified download from UCI. |
| `cb_2018_us_state_500k.zip` | U.S. state boundaries, used for the regional map. |

## Sources

- **Communities and Crime Unnormalized**, UCI Machine Learning Repository (CC BY 4.0).
  https://archive.ics.uci.edu/dataset/211/communities+and+crime+unnormalized
- **2018 Cartographic Boundary File: States, 1:500,000**, U.S. Census Bureau.
  https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_state_500k.zip

## Rebuilding crimedata.csv

To recreate `crimedata.csv` from the original download, run this from the project's main folder:

```
python scripts/make_dataset.py data/communities+and+crime+unnormalized.zip
```