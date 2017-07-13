import os # The only purpose here is for renaming files
import requests # Get Page
import datetime # Get Time
from tqdm import tqdm # Progress Bar
from zipfile import ZipFile # Unzip KMZ


def download(file_name):
    # Url
    url = 'http://opendata.cwb.gov.tw/govdownload?dataid=O-A0039-001&authorizationkey=rdec-key-123-45678-011121314'
    # Mock this scrapy as a Mac using Chrome
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    # GET: Url
    g = requests.Session().get(url, stream=True, headers=headers)

    # Download data
    print("下載中...")
    with open(file_name, "wb") as f:
        for data in tqdm(g.iter_content()):
            f.write(data)

def kmz2kml(kmz_file_name, kml_file_name, json_file_name):
    print("解壓縮中...\n")
    # Define which file to Unzip
    kml = ZipFile(kmz_file_name, 'r')
    # Unzip KMZ
    kml.extract('doc.kml', './KML')
    # Close it
    kml.close()
    # Rename
    os.rename('./KML/doc.kml', kml_file_name)


def kml2txt(kml_file_name):
    kml = os.path.join(kml_file_name)
    with open(kml) as f:
        doc = parser.parse(f)
        print(root.Document.Folder.Placemark)

if __name__ == '__main__':
    # Get datetime now
    time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    print("現在時間：" + time + "\n")
    # Filenames
    kmz_file_name = "./KMZ/" + time + ".kmz"
    kml_file_name = "./KML/" + time + ".kml"
    json_file_name = "./JSON/" + time + ".geojson"
    txt_file_name = "./TXT/" + time + ".txt"
    # Get file on web
    download(kmz_file_name)
    # Unzip KMZ
    kmz2kml(kmz_file_name, kml_file_name, json_file_name)


