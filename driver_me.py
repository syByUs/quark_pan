
# -*- coding: utf-8 -*-
import time
from coze import CozeManager
from excel_manager import ExcelManager
import asyncio
from pipes import quote
import re
import sys
import httpx
from prettytable import PrettyTable
from tqdm import tqdm
from feishu import FeishuQuarkResourceManager
from post_bot import PostManager
from quark import QuarkPanFileManager
from quark_login import QuarkLogin, CONFIG_DIR
import json
from typing import List, Dict, Union, Tuple, Any

FOLDE_NAME_ID = {
    "图书": "<你自己夸克网盘的文件id>"
}

def search_quark_url(text):
    pattern = r'pan\.quark\.cn/s/[a-zA-Z0-9]+'  # 匹配字母数字ID
    match = re.search(pattern, text)
    if match:
        print("提取的链接:", match.group())
        link = match.group()
        """
        判断输入是否合法的 pan.quark.cn 链接
        示例合法链接: pan.quark.cn/s/67fe4f39e495
        """
        pattern = r'^pan\.quark\.cn/.*$'
        if bool(re.match(pattern, link)):
            return link
        else:
            return None
    else:
        print("未找到匹配的链接")
        return None


# 代码直接转存，不需要输入
async def driver_me(link, record_id=None):
    if link is None:
        return
    excel_manager = ExcelManager(file_path='E:/QuarkPanTool/resource/resource.xlsx')
    quark_manager = QuarkPanFileManager(headless=False, slow_mo=500)
    # 1、获取文件名
    data_list, pwd_id, stoken = await quark_manager.get_share_file_name(link)
    data = data_list[0]
    file_name = data.get("file_name", "").strip()
    print(file_name)

    #2、判断文件名是否已经存在
    records = excel_manager.get_record_by_title(file_name)
    print(records, 'records')
    if excel_manager.exists_by_title(file_name):
        excel_manager.increment_count(file_name)
        print(f"【{file_name}】文件已存在")
        return
    print(f"【{file_name}】文件不存在，继续下一步")
    
    #3、分析归纳文件名属于哪一种类型，通过coze工作流实现
    try:
        coze_manager = CozeManager(workflow_id="<你自己夸克网盘的工作流id>")
        parameters = {"input": file_name}
        wf_result, _, _ = coze_manager.run_workflow(parameters=parameters)
        # print(f"Data type of result: {type(wf_result)}")  # Print the data type of result
        """
        {"des":"《漫画数学王》全三册是由韩国善友教育编辑部编写、崔栽宏绘制，北京联合出版有限公司出版的数学启蒙读物。该书通过漫 
    画形式将数学知识融入趣味故事中，帮助青少年在轻松阅读中掌握数学思维，适合中小学生课外拓展学习。","img_list":"[\"https://p3-search.byteimg.com/img/labis/b8ce2106f31cc7783dcadc60cab1bb39~480x480.JPEG\",\"https://p3-search.byteimg.com/img/labis/304c2eefc9a185cea6cc54215642d727~480x480.JPEG\"]","title":"图书"}
        """
        # 解析wf_result
        wf_result_json = json.loads(wf_result)
        category = wf_result_json.get('category')
        title = file_name
        des = wf_result_json.get('des')
        img_list = wf_result_json.get('img_list')
    except Exception as e:
        print("工作流出错:", e)
        title = file_name
        category = "图书"
        des = ""
        img_list = []
    if isinstance(img_list, str) and len(img_list) > 0:
        img_list = json.loads(img_list)

    #4、切换到对应类型的文件夹，不需要切换，知道对应的文件夹id就可以
    folder_id = FOLDE_NAME_ID.get(category)
    if folder_id is None:
        folder_id = FOLDE_NAME_ID.get("图书")

    #5、转存
    fid_list = [i["fid"] for i in data_list]
    share_fid_token_list = [i["share_fid_token"] for i in data_list]
    task_id = await quark_manager.get_share_save_task_id(pwd_id, stoken, fid_list, share_fid_token_list,
                                                            to_pdir_fid=folder_id)
    json_data = await quark_manager.submit_task(task_id)

    #5.1 解析转存结果
    data = json_data['data']
    # print("data：", data, type(data))
    save_as_data = data['save_as']
    to_pdir_fid = save_as_data['to_pdir_fid']
    to_pdir_name = save_as_data['to_pdir_name']
    save_as_top_fids = save_as_data['save_as_top_fids']
    #6、转存成功后，获取转存后的分享地址
    pj_url = pinjie_url(to_pdir_fid, to_pdir_name, save_as_top_fids, file_name)
    
    #7、生成分享地址，如果是文件夹，则进行这一步，否则不进行
    time.sleep(5) # 等待转存完成，防止分享失败
    quark_url = await gen_share_url(quark_manager, pj_url)
    if quark_url is None:
        print("分享地址为空，不进行下一步")
        return

    #8、将名称和地址写入到excel中
    excel_data = {
        'title': title,
        'des': des,
        'img': json.dumps(img_list),
        'quark': quark_url,
        'baidu': "",
        'category': category
    }
    excel_manager.update_or_insert([excel_data])

    #8.1、将名称和分享地址写入到飞书表格，方便资源资源同步
    coze_fs_sheet = CozeManager(workflow_id="<你自己的飞书表格工作流id>")
    spreadsheet_token = "<你自己的飞书表格token>"
    parameters = {"sheet_name": "Sheet1", "name": title, "des": des, "quark": quark_url, "category": category, "baidu": "", "spreadsheet_token": spreadsheet_token}
    _, _, _ = coze_fs_sheet.run_workflow(parameters=parameters)

    #8.2 更新表格为已转存
    feishu_manager.update_table_record(record_id)

    #9 发推、发电报群
    post_bot = PostManager()
    if category == "图书":
        post_data = post_bot.gen_book_img_for_social(excel_data.get('title'))
        post_data['content'] = f"{des}\n链接：{quark_url}"
    else:
        post_data = {
            "title": title,
            "content": f"{des}\n链接：{quark_url}"
        }
        if len(img_list) > 0:
            post_data['pic1'] = img_list[0]
        if len(img_list) > 1:
            post_data['pic2'] = img_list[1]
        if len(img_list) > 2:
            post_data['pic3'] = img_list[2]
    print("post_data：", post_data)
    await post_bot.post(post_data)

    

async def gen_share_url(manager: QuarkPanFileManager, url: str):
    to_dir_id = manager.folder_id
    url_encrypt = 1 # 不加密
    _expired_type = 1 # 永久
    password = ""
    _traverse_depth = 0
    share_url = await manager.share_run(url.strip(), folder_id=to_dir_id, url_type=int(url_encrypt), 
                      expired_type=int(_expired_type), password=password, traverse_depth=_traverse_depth)
    print("分享地址：", share_url)                      
    return share_url

# 拼接url
def pinjie_url(to_pdir_fid, to_pdir_name, save_as_top_fid, file_name):
    """
    https://pan.quark.cn/list#/list/all/9909d15a2f9d4730a932733ed0ab5ed7-%E5%9B%BE%E4%B9%A6/3a260b9d50cc4c81aa088a51e8622157-%E5%BE%81%E6%9C%8D%E4%B8%8E%E9%9D%A9%E5%91%BD%E4%B8%AD%E7%9A%84%E9%98%BF%E6%8B%89%E4%BC%AF%E4%BA%BA(1)
    """
    to_pdir = f"{to_pdir_fid}-{to_pdir_name}"
    top_fid = f"{save_as_top_fid[0]}-{file_name}"
    url = f"https://pan.quark.cn/list#/list/all/{to_pdir}/{top_fid}"
    print("pinjie_url：", url)
    # url encoder
    return url

if __name__ == '__main__':

    feishu_manager = FeishuQuarkResourceManager()
    
    while True:
        type = input("请输入类型，1从飞书表格获取分享链接， 2自己输入链接")
        if type == "1":
            while True:
                try:
                    items = feishu_manager.search_table_record()
                    for item in items:
                        original_link = item.get("quark_share_link")
                        record_id = item.get("record_id")
                        link = search_quark_url(original_link)
                        if link is not None:
                            asyncio.run(driver_me(link=link, record_id=record_id))
                        else:
                            print(f"输入的链接不是quark链接，请重新输入:{original_link}")
                        continue
                except Exception as e:
                    print("飞书表格获取失败:", e)
                print("等待60秒后继续获取...")
                time.sleep(60)
        elif type == "2":
            original_link = input("请输入待分享的链接：")
            link = search_quark_url(original_link)
            if link is not None:
                asyncio.run(driver_me(link))
            else:
                print(f"输入的链接不是quark链接，请重新输入:{original_link}")
                continue
        else:
            print("输入错误，请重新输入")
            continue
        time.sleep(3)