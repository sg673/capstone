from enum import Enum
from pathlib import Path
import pandas as pd
import os
from sqlalchemy import create_engine
import streamlit as st

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
        secrets = st.secrets

        engine = create_engine(
            f"postgresql://{secrets['SOURCE_DB_USER']}:{secrets['SOURCE_DB_PASSWORD']}@"
            f"{secrets['SOURCE_DB_HOST']}:{secrets['SOURCE_DB_PORT']}/{secrets['SOURCE_DB_NAME']}"
        )
        with engine.connect() as conn:
            data = pd.read_sql("SELECT * FROM de_2506_a.sam_capstone", conn)
            return data

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


if __name__ == "__main__":
    print(get_data().shape)
