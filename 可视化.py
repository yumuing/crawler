from matplotlib.ticker import MultipleLocator
from pymongo import MongoClient
import matplotlib.pyplot as plt
import matplotlib
import re
#连接MongoDB数据库
client = MongoClient('localhost', 27017)
db = client.get_database("lianjia2")
col = db.get_collection("loupan")
guandao=[{
    "$group":{"_id":"$type","num":{"$sum":1}}
}]
lists=col.aggregate(guandao)
print(lists)
num_list1 = []
type1=[]#存放类型
sum1=[]#存放个数
num1=0
for list in lists:
    # num_list1.append(list)
  print(list)
  if (list["_id"]=="商业" or list["_id"]=="商业类"):
      num1 += list["num"]

  else:
      sum1.append(list["num"])
      type1.append(list["_id"])
sum1.append(num1)
name1="商业"
type1.append(name1)
print(sum1)
print(type1)
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
plt.pie(sum1,labels=type1,autopct='%1.1f%%',shadow=False,startangle=150)
plt.title("武汉各类型房源占比")
plt.savefig("武汉各类型房源占比饼状图.png")
plt.show()
#柱形
pipeline = [
    {"$match":
        {
            "type": "住宅",
            "price": {"$ne": 0}
        }
    },#过滤掉房价待定且不是住宅用途的楼盘
    {"$group":
        {
            "_id": "$area1",
            "avgPrice": {"$avg": "$price"},
            "MaxPrice": {"$max": "$price"}
        }
    },
]
lists = col.aggregate(pipeline)
label_list = []
num_list1 = []
num_list2 = []
#获取聚合后的数据并插入label_list ，num_list1，num_list2，用于纵横坐标显示。
for list in lists:
    label_list.append(list['_id'])


    num_list1.append(round(list['avgPrice'], 1))
    num_list2.append(list['MaxPrice'])
print(num_list2)


matplotlib.rcParams['font.sans-serif'] = ['SimHei']
x = range(len(num_list1))

#绘制条形图 :条形中点横坐标；height:长条形高度；width:长条形宽度，默认值0.8；label:为后面设置legend准备
plt.figure(figsize=(18,10))
ax = plt.axes()
rects1 = plt.bar(x, height=num_list1, width=0.4, alpha=0.8, color='red', label="平均房价")
rects2 = plt.bar([i + 0.4 for i in x], height=num_list2, width=0.4, color='green', label="最高房价")

plt.ylim(0, max(num_list2)+8000)     # y轴取值范围
plt.ylabel("价格")

#设置x轴刻度显示值；参数一：中点坐标；参数二：显示值
plt.xticks([index + 0.2 for index in x], label_list)
plt.xlabel("区域",labelpad = 20)
plt.title("武汉地区房价")
plt.legend()     # 设置题注

for rect in rects1:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2, height+1, str(height), ha="center", va="bottom")
for rect in rects2:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2, height+1, str(height), ha="center", va="bottom")
# #显示条形图
plt.savefig("武汉地区房价水平柱形图.png")
plt.show()