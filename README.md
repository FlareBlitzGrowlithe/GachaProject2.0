# GachaProject2.0
### 简介
一个简单的为本固桌原创桌游而写的抽卡小工具，2.0版本，基于SQLite和Bootstrap，使用了flask作为后端，支持一些基础的后台和kp管理功能，请调用register手动进行用户注册
### 特性
- 单抽
- 十连
- 小怪池和boss池
- 更易用的结果表单
- 可下载抽卡结果
- 可进行库存管理
- 添加道具商店功能
### 使用
```
npm install
python app.py
```
成功运行后页面将显示在3155端口。
### 替换卡池
在/database下建立自己的数据库equipment.db, inventory.db, user.db
表单具体条目详见/utils/equipment.py, /utils/inventory.py, /utils/user.py

