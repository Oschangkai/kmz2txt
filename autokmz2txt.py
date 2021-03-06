import os # The only purpose here is for renaming files
import requests # Get Page
import datetime # Get Time
from tqdm import tqdm # Progress Bar
from zipfile import ZipFile # Unzip KMZ
from fastkml import kml # Parse KML

def download(kmz_file_name):
    print("連線中...")
    # Url
    url = 'http://opendata.cwb.gov.tw/govdownload?dataid=O-A0039-001&authorizationkey=rdec-key-123-45678-011121314'
    # Mock this scrapy as a Mac using Chrome
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    # GET: Url
    g = requests.Session().get(url, stream=True, headers=headers)

    # Download data
    print("下載中...")
    with open(kmz_file_name, "wb") as f:
        for data in tqdm(g.iter_content()):
            f.write(data)
    print("下載完成！\n")

def kmz2kml(kmz_file_name, kml_file_name):
    print("解壓縮中...")
    # Define which file to Unzip
    kml = ZipFile(kmz_file_name, 'r')
    # Unzip KMZ
    kml.extract('doc.kml', './KML')
    # Close it
    kml.close()
    # Rename
    os.rename('./KML/doc.kml', kml_file_name)
    print("解壓縮完成！\n")


def kml2txt(kml_file_name, txt_file_name):
    print("正在解析資料...")
    # Calculate file size
    b = int(os.path.getsize(kml_file_name))
    # Open file(Readonly)
    f = os.open(kml_file_name, os.O_RDONLY)
    # Read file as binary
    kml_string = os.read(f,b)
    # Close file
    os.close(f)

    # Create the KML object to store the parsed result
    k = kml.KML()
    # Read in the KML string
    k.from_string(kml_string)

    # Filter Data
    dataset = list(k.features())
    dataset = list(dataset[0].features())
    dataset = list(dataset[0].features())
    
    txt = "[項次]\t[閃電種類]\t[日期 Y-M-D]\t[時間 H:M:S:s]\t[強度 kAmp]\t[經度]\t[緯度]\n"

    # if data collected
    if len(dataset):
        print("搜集到共 "+str(len(dataset))+" 筆資料，寫入中...")

        record_no = 1 # 項次
        
        for ds in tqdm(dataset):
            data = str.split(ds.description)
            record_type = data[1] + "閃電" # 閃電種類
            record_date = data[3] # 日期 Y-M-D
            record_time = data[4] # 時間 H:M:S:s
            record_kAmp = data[6] # 強度 kAmp
            record_longitude = data[9] # 經度
            record_latitude = data[11] # 緯度

            txt += str(record_no) + "\t"
            txt += record_type + "\t" + record_date + "\t" + record_time + "\t"
            txt += record_kAmp + "\t"
            txt += record_longitude + "\t" + record_latitude + "\t"
            txt += "\n"
            record_no += 1
    else:
        print("0 筆資料，無需新增紀錄")
    
    # Write File
    with open(txt_file_name, "w") as f:
        f.write(txt)

    print("\n")

if __name__ == '__main__':
    print("====================")
    print("     閃電資料爬蟲     ")
    print("====================")
    # Get datetime now
    time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    print("現在時間：" + time + "\n")
    # Filenames
    kmz_file_name = "./KMZ/" + time + ".kmz"
    kml_file_name = "./KML/" + time + ".kml"
    txt_file_name = "./TXT/" + time + ".txt"
    # Get file on web
    download(kmz_file_name)
    # Unzip KMZ
    kmz2kml(kmz_file_name, kml_file_name)
    # Parse KML
    kml2txt(kml_file_name, txt_file_name)
    print("程式結束")

