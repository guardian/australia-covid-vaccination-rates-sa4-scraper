import camelot
import os
import pandas as pd
import numpy as np
import requests
from datetime import datetime

MYDIR = ("pdfs")
CHECK_FOLDER = os.path.isdir(MYDIR)

# If folder doesn't exist, then create it.

if not CHECK_FOLDER:
    os.makedirs(MYDIR)
    print("created folder : ", MYDIR)

else:
    print(MYDIR, "folder already exists.")

files = os.listdir("pdfs/")

urls = [
"https://www.health.gov.au/sites/default/files/documents/2021/08/covid-19-vaccination-geographic-vaccination-rates-2-august-2021.pdf",
"https://www.health.gov.au/sites/default/files/documents/2021/08/covid-19-vaccination-geographic-vaccination-rates-9-august-2021.pdf"
]

for url in urls:
	if url.split("/")[-1] not in files:
		print("getting", url)
		r = requests.get(url)
		file = open("pdfs/" + url.split("/")[-1], "wb")
		file.write(r.content)
		file.close()

new_files = os.listdir("pdfs/")
print(new_files)
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def cleanDF(df):
	df.columns = ['State', 'SA4', 'At_least_one_dose_15', 'Fully_vaccinated_15']
	df = df.drop(df.index[0])
	# df = df.replace('', np.nan)
	# df = df.dropna()
	return df

def readPDF(filename):
	dataframes = []
	date_str = filename.split("geographic-vaccination-rates-")[1].split(".pdf")[0]
	date_obj = datetime.strptime(date_str, "%d-%B-%Y")
	new_date_str = date_obj.strftime("%Y-%m-%d")
	print(new_date_str)
	for page in range(2,11):
		print(page)
		tables = camelot.read_pdf(filename, pages=f"{page}")
		dataframes.append(cleanDF(tables[0].df))

	merge = pd.concat(dataframes, ignore_index=True)
	merge['date'] = new_date_str
	return merge

dataframes = []

for file in new_files:
	print("scraping", file)	
	dataframes.append(readPDF("pdfs/" + file))

merge = pd.concat(dataframes, ignore_index=True)

merge['At_least_one_dose_15'] = merge['At_least_one_dose_15'].str.rstrip('%').astype('float') / 100
merge['Fully_vaccinated_15'] = merge['Fully_vaccinated_15'].str.rstrip('%').astype('float') / 100

merge['At_least_one_dose_15'] = merge['At_least_one_dose_15'].round(3)
merge['Fully_vaccinated_15'] = merge['Fully_vaccinated_15'].round(3)
merge.sort_values('date', inplace=True)
merge.to_csv('geographic_vax_rates.csv', index=False)


print("Done. PDFs scraped")