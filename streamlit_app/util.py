from enum import Enum
from pathlib import Path
import pandas as pd
import os


class AccessType(Enum):
    DATABASE = 1
    FILE = 2
    ETL = 3


# AI generated
STATE_NAMES = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
    'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut',
    'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii',
    'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
    'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine',
    'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan',
    'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri',
    'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
    'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico',
    'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota',
    'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania',
    'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota',
    'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
    'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
    'WI': 'Wisconsin', 'WY': 'Wyoming'
}


def get_data(access: AccessType = AccessType.DATABASE) -> pd.DataFrame:
    if access == AccessType.DATABASE:
        # Add connection to database
        print("not availabe yet")
        return pd.DataFrame()

    if access == AccessType.FILE:
        file = Path(os.getcwd()).parent / "etl_process" / "data" / "output" / "merged_data.csv"
        if not file.exists():
            raise FileNotFoundError(f"file not found {file}")
        df = pd.read_csv(file, encoding="latin-1", index_col=0)
        return df

    if access == AccessType.ETL:
        # run the etl pipeline and get the dataframe directly
        print("not availabe yet")
        return pd.DataFrame()
