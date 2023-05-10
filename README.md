# 使用方法
文件说明：
+ add.txt:房源经纬度数据
+ fake_useragent,json:随机ua列表
+ readme.md:说明文件
+ thermalMap.html:热力图网页
+ toTxt.py:将MongDB的房源地址数据转换成经纬度，并存入add.txt中
+ 可视化.py:将MongDB的房源数据进行数据分析，并可视化为武汉各类型房源占比饼状图、武汉地区房价水平柱形图
+ png：结果图片文件
+ 爬取数据.py:爬取武汉链家房源数据，共729个房源数据

自行准备好运行环境，如下：
+ 启动MongDB服务以及Redis服务
+ 安装依赖
+ 运行 proxy_pool 开源库：随机ip

运行顺序：
+ 爬取数据（爬取数据.py）：共729个武汉房源数据
+ 可视化(可视化.py)：武汉各类型房源占比饼状图、武汉地区房价水平柱形图
+ 热力图(toTxt.py)：往add.txt写入所有房源经纬度，自行写入到thermalMap.html要求位置，运行该html即可获得热力图

![热力图](https://s2.loli.net/2023/05/10/D1GMOwenoyX9cbf.png)

![武汉地区房价水平柱形图](https://s2.loli.net/2023/05/10/6pBlOaVK7CbTmSM.png)

![武汉各类型房源占比饼状图](https://s2.loli.net/2023/05/10/B8yW4TuELlaGS1c.png)
