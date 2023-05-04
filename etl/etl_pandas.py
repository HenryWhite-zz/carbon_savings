import pandas as pd

def extract_data(file_path):
    # Read in the Excel file using pandas
    data = pd.read_excel(file_path)
    return data

def transform_data(data):
    # Apply some transformations to the data using pandas
    return data
