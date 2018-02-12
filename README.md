neteaseMusicCommentsSpider
=====
*A simple NeteaseCloudMusic comments spider.*

用法
-----
1. 添加歌曲 ID 到`master/taskMaster.py`的`songIdList`当中。
2. `python master/taskMaster.py`
3. ` python worker/taskWorker.py`
	
**注意：**需要运行 MongoDB。

自定义 MongoDB 连接？
-----
请修改`master/mongoDb.py`。

其他
-----
建议分布式，小心网易云音乐封禁 IP 。。
