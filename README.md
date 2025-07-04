# QuarkPan

[![Python Version](https://img.shields.io/badge/python-3.11.6-blue.svg)](https://www.python.org/downloads/release/python-3116/)
[![Latest Release](https://img.shields.io/github/v/release/syByUs/quark_pan)](https://github.com/syByUs/quark_pan/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/syByUs/quark_pan/total)](https://github.com/syByUs/quark_pan/releases/latest)
![GitHub Repo stars](https://img.shields.io/github/stars/syByUs/quark_pan?style=social)


quark_pan是一个简单易用的小工具，旨在帮助用户快速批量转存分享文件，同时结合coze工作流实现自动分类，自动同步到知识库/数据库。


### 安装依赖
```
pip install -r requirements.txt
playwright install firefox
```

### 运行
1、目的是为了登录夸克网盘，并获取cookie，以便后续使用
```
python quark.py
```

2、夸克网盘操作逻辑，参考[ihmily](https://github.com/ihmily/QuarkPanTool)
<br>
启动逻辑可参考[readme](https://github.com/syByUs/QuarkPanTool/edit/main/README.md)

3、启动夸克网盘分享
```
python driver_me.py
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

### 代码逻辑
可以参考公众号文章，[点我](https://mp.weixin.qq.com/s/R3IAUg8TuipiEAIxkby3Bg)
<br>
![98b96a10d96d62b7c7822c6d5fc767d](https://github.com/user-attachments/assets/8f255389-b5c0-42dd-953f-0f4d1cb2e7c8)

## Coze平台使用方法
### Coze商店，资源自动分享
[点我直达](https://www.coze.cn/store/agent/7523165962342776847?bid=6gpuleclo8g16)
<br>
操作页面，输入cookies，点击发送按钮，即会将网盘链接自动分享到你的网盘；
![image](https://github.com/user-attachments/assets/5f8439bd-55fa-40c7-a876-78bcb1e020d7)
<br>
### 如何获取cookie
[点我查看](https://github.com/spider-ios/autox-release/blob/main/cookie-helper/README.md)



## 许可证

quark_tool 使用 [Apache-2.0 license](https://github.com/ihmily/QuarkPanTool#Apache-2.0-1-ov-file) 许可证，详情请参阅 LICENSE 文件。

# 免责声明
<div id="disclaimer"> 

## 1. 项目目的与性质
本项目（以下简称“本项目”）是作为一个技术研究与学习工具而创建的，旨在探索和学习使用；

## 2. 法律合规性声明
本项目开发者（以下简称“开发者”）郑重提醒用户使用本项目时，严格遵守中华人民共和国相关法律法规，包括但不限于《中华人民共和国网络安全法》、《中华人民共和国反间谍法》等所有适用的国家法律和政策。用户应自行承担一切因使用本项目而可能引起的法律责任。

## 3. 使用目的限制
本项目严禁用于任何非法目的或非学习、非研究的商业行为。本项目不得用于任何形式的非法侵入他人计算机系统，不得用于任何侵犯他人知识产权或其他合法权益的行为。用户应保证其使用本项目的目的纯属个人学习和技术研究，不得用于任何形式的非法活动。

## 4. 免责声明
开发者已尽最大努力确保本项目的正当性及安全性，但不对用户使用本项目可能引起的任何形式的直接或间接损失承担责任。包括但不限于由于使用本项目而导致的任何数据丢失、设备损坏、法律诉讼等。

## 5. 知识产权声明
本项目的知识产权归开发者所有。本项目受到著作权法和国际著作权条约以及其他知识产权法律和条约的保护。用户在遵守本声明及相关法律法规的前提下，可以下载和使用本项目。

## 6. 最终解释权
关于本项目的最终解释权归开发者所有。开发者保留随时更改或更新本免责声明的权利，恕不另行通知。
</div>


