# 進行網絡連綫
import urllib.request as request
import json
src="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json"
with request.urlopen(src) as response:
    data=json.load(response)

# 題目1）把JSON格式資料裏的資料逐個取出
attraction=data["result"]["results"]
att_name=[]
for name in attraction:
    attraction_name=name["stitle"]
    att_name.append(attraction_name)

att_area=[]
for add in attraction:
    area=add["address"]
    att_area.append(area[5:8])

att_long=[]
for longitude in attraction:
    longi=longitude["longitude"]
    att_long.append(longi)

att_lat=[]
for latitude in attraction:
    lat=latitude["latitude"]
    att_lat.append(lat)

att_photo=[]
for pho in attraction:
    photo=pho["file"]
    att_photo.append(photo[:photo.index('https',6)])

# 載入csv模組，寫入attraction.csv格式檔案
import csv
with open("attraction.csv",mode="w",newline="",encoding="utf-8") as detail:
    for x in range(0,len(att_name)):
        att_list=csv.writer(detail)
        att_list.writerow([att_name[x],att_area[x],att_long[x],att_lat[x],att_photo[x]])

# 題目2）把所有景點(key)的捷運站名稱(value)放進字典，以供配對
mrt_dic={}
for att in attraction:
    mrt_dic[att["MRT"]]=[]

# 把所有想印出來的資料放到mrt_dic[att["MRT"]]的value(list)裏面
for att in attraction:
    mrt_dic[att["MRT"]].append(att["MRT"])
    mrt_dic[att["MRT"]].append(att["stitle"])

# 用mrt_dic去loop 把所有的value逐一印出來
with open("mrt.csv",mode="w",newline="",encoding="utf-8") as mrt: 
    for m in mrt_dic: 
        station_map=csv.writer(mrt)
        station_map.writerow(mrt_dic[m])