import requests
import io
from zipfile import ZipFile

# Get zipped folder containing Balancing_Authority_2021.xlsx file
url = 'https://www.eia.gov/electricity/data/eia861/zip/f8612021.zip'
r = requests.get(url)
zip_file = ZipFile(io.BytesIO(r.content))
zip_file.extract('Balancing_Authority_2021.xlsx', 'data/source')
