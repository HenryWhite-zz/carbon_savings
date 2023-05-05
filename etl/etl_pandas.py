import requests
import io
from zipfile import ZipFile
import pandas as pd
import os


def extract_excel_zip(url, file):
    # Extract excel file from a zipped folder
    # Check if it already exists
    if not os.path.isfile(f'data/source/{file}'):
        r = requests.get(url)
        zip_file = ZipFile(io.BytesIO(r.content))
        zip_file.extract(file, 'data/source')

    # Create dataframe from excel file
    data = pd.read_excel(f'data/source/{file}')
    return data


def transform_ba(df):
    df.columns = ['year', 'ba_id', 'ba_code', 'state', 'ba_name']
    return df
