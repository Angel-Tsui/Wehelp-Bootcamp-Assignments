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
# print(att_name)

att_area=[]
for add in attraction:
    area=add["address"]
    att_area.append(area[5:8])
# print(att_area)

att_long=[]
for longitude in attraction:
    longi=longitude["longitude"]
    att_long.append(longi)
# print(att_long)

att_lat=[]
for latitude in attraction:
    lat=latitude["latitude"]
    att_lat.append(lat)
# print(att_lat)

att_photo=[]
for pho in attraction:
    photo=pho["file"]
    att_photo.append(photo[:photo.index('https',6)])
# print(att_photo)

# 載入csv模組，寫入attraction.csv格式檔案
import csv
with open("attraction.csv",mode="w",newline="",encoding="utf-8") as detail:
    for x in range(0,len(att_name)):
        att_list=csv.writer(detail)
        att_list.writerow([att_name[x],att_area[x],att_long[x],att_lat[x],att_photo[x]])

# 題目2）把JSON格式資料裏的資料逐個取出 - 捷運站
att_mrt=[]
for mrt in attraction:
    station=mrt["MRT"]
    att_mrt.append(station)
# print(att_mrt)

# 把所有景點(key)的捷運站名稱(value)放進字典，以供配對
mrt_dic={}
for att in attraction:
    mrt_dic[att["stitle"]]=att["MRT"]
    # print(mrt_dic[att["stitle"]])

# 讓每一個att_mtr都生成一個獨立的array
# 如果mtr_dic[att["stitle"]](value)跟att_mrt裏面的字對上，就把s推到array裏面
for s in mrt_dic:
    print(s) #印出mrt_dic的所有key

# 最後把所有belong to同一個捷運站的景點推進mrt.csv裏面同一個row
# 載入csv模組，寫入mrt.csv格式檔案
# import csv
# with open("mrt.csv",mode="w",newline="",encoding="utf-8") as mrt:
#     for y in range(0,len(att_mrt)):
#         att_m=csv.writer(mrt)
#         att_m.writerow([att_mrt[y],mrt_dic[y[]]])




# for k in att_mrt:
#     # k=[]
#     globals()[str(k)]=att_mrt[k]
#     print(globals()[str(k)])

#     for n in mrt_dic[att["stitle"]]:
#         if n==k:
#             k.append(n)
# print(k)

#     for mrt_dic[att["stitle"]] in range(0,len(att_mrt)):
#         mrt_all=mrt_dic[att["stitle"]]
#         mrt_all.append(mrt_dic[att])
# print(mrt_all)

# for m in mrt_dic:
#     m=[]
#     if mrt_dic[m] in m:
#         m.append(mrt_dic[m])
# print(m)

