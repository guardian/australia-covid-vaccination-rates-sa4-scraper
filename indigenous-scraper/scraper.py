import pdfquery
import requests
import lxml.etree
import os

MYDIR = ("pdfs")
CHECK_FOLDER = os.path.isdir(MYDIR)

# If folder doesn't exist, then create it.

if not CHECK_FOLDER:
    os.makedirs(MYDIR)
    print("created folder : ", MYDIR)

else:
    print(MYDIR, "folder already exists.")

# Indigenous 16+ population estimates from ABS ERP for 2021, will be replaced with medicare/AIR data at some point

indigPop = {
    "NSW":188410,
    "VIC":42751,
    "QLD":158477,
    "SA":30250,
    "WA":73154,
    "TAS":20370,
    "NT":55357,
    "ACT":5914
}

files = os.listdir("pdfs/")

for file in files:
    with open("pdfs/" + file, "rb") as pdffile:
        fileData=pdffile.read()
     
    xmldata = scraperwiki.pdftoxml(fileData)

