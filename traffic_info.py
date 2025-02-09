import requests
from bs4 import BeautifulSoup

# yahooの沖縄県渋滞情報を取ってくる
yahoo_URL = "https://roadway.yahoo.co.jp/traffic/area/11/road/1091018/list?p=0.17298644687684828,0.4515545670543588&z=13&scale=4&moved=1&bbox=0.09573904550256884,0.3394596879047356,0.2502335338095918,0.5636494462053179"
response = requests.get(yahoo_URL)
response.encoding = response.apparent_encoding 


# BeautifulSoupでHTMLを解析しクラスなどから変数に保存
soup = BeautifulSoup(response.text, "html.parser")
traffic_info = soup.find_all("table", class_="rinfo-table")


# 得た情報をリストに保存し加工
info_li  = []
for info in traffic_info:
    str_info = str(info.text.strip())
    info_li.append(str_info)        
split_traffic_list = [item.split("\n") for item in info_li]


print(split_traffic_list)