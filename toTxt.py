import requests
import json
import re

from pymongo import MongoClient

AK = 'P9ahwxvm4j9GC2n9PhI7swK9VcgZLvsH'
client = MongoClient('localhost', 27017)
db = client.get_database("lianjia2")
col = db.get_collection("loupan")
pipeline = [
    {"$match":
        {
            "type": "住宅",
            "price": {"$ne": 0}
        }
    },#过滤掉房价待定且不是住宅用途的楼盘
    # {"$group":
    #     {
    #         "_id": "$area1",
    #         "avgPrice": {"$avg": "$price"},
    #         "MaxPrice": {"$max": "$price"},
    #         "detail_place":"$detail_place"
    #     }
    # },
]
lists = col.aggregate(pipeline)
Note = open('add.txt', mode='w+')
for list in lists:
    # print(list["detail_place"])
    address =list["detail_place"]
    url = 'http://api.map.baidu.com/geocoding/v3/?address={}&output=json&ak={}&callback=showLocation'.format(address,AK)
    res = requests.get(url)
    # print(res.text)
    results = json.loads(re.findall(r'\((.*?)\)',res.text)[0])
    if not 'msg' in results.keys():
        Note.write("{\"lng\":"+str(results['result']['location']['lng'])+",\"lat\":"+str(results['result']['location']['lat'])+",\"count\":50},\n")
        print("{\"lng\":"+str(results['result']['location']['lng'])+",\"lat\":"+str(results['result']['location']['lat'])+",\"count\":50}")

Note.close()