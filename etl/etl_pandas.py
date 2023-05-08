import requests
import io
from zipfile import ZipFile
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
env_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path=env_path)

# Set API key
api_key_eia = os.getenv('API_KEY_EIA')


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
    # Rename columns
    df.columns = ['year', 'ba_id', 'ba_code', 'state', 'ba_name']

    # Get list of BAs supported by API
    ba_list2 = extract_ba_list(api_key_eia)

    # Remove any BAs not supported by the API
    df = df[df['ba_code'].isin(ba_list2['id'])]

    return df


def extract_ba_list(api_key):
    # Get list of all Balancing Authorities from the API
    url = ('https://api.eia.gov/v2/electricity/rto/daily-region-data/facet/'
           'respondent/?api_key=' + api_key)
    r = requests.get(url)
    ba_json_data = r.json()
    ba_list = pd.DataFrame.from_dict(ba_json_data)
    ba_list = pd.DataFrame(ba_list.loc['facets', 'response'])
    return ba_list
