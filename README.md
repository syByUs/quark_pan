## python版本要求python 3.10
### 安装依赖
```
pip install -r requirements.txt
playwright install firefox
```

### 运行
```
python quark.py
目的是为了登录夸克网盘，并获取cookie，以便后续使用
```

```
夸克网盘操作逻辑，完全参考[ihmily](https://github.com/ihmily/QuarkPanTool)
启动逻辑可以参考他的readme
```

```
python driver_me.py
启动夸克网盘分享
```

### 文件说明
```
coze.py coze的逻辑处理，需要秘钥
feishu.py 飞书表格的逻辑处理，需要秘钥
post_bot.py 自动发帖到x和tg的逻辑处理，不需要秘钥
tg_bot.py 电报的逻辑处理，需要秘钥
x_h_bot.py X发推的逻辑处理，不需要秘钥
quark_login.py 登录夸克网盘并获取cookie
quark.py 夸克网盘的主要逻辑处理
driver_me.py 启动夸克网盘分享
```

### 交互逻辑
![98b96a10d96d62b7c7822c6d5fc767d](https://github.com/user-attachments/assets/8f255389-b5c0-42dd-953f-0f4d1cb2e7c8)
可以参考公众号文章，[点我](https://mp.weixin.qq.com/s/R3IAUg8TuipiEAIxkby3Bg)




