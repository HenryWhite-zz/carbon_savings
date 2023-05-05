import requests
import io
from zipfile import ZipFile
import pandas as pd

def extract_excel_zip(url, file):
    # Extract excel file from a zipped folder
    r = requests.get(url)
    zip_file = ZipFile(io.BytesIO(r.content))
    zip_file.extract(file, 'data/source')

    # Create dataframe from excel file
    data = pd.read_excel(f'data/source/{file}')
    return data


def transform_ba(df):
    df.columns=['year', 'ba_id', 'ba_code', 'state', 'ba_name']
    return df

# Temporarily calling functions for easy verification
df = extract_excel_zip('https://www.eia.gov/electricity/data/eia861/zip/f8612021.zip',
                  'Balancing_Authority_2021.xlsx')

df = transform_ba(df)

print(df)