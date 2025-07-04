import random
import time
from coze import CozeManager
from x_h_bot import ChromeInstanceManager
from tg_bot import TelegramBot
import asyncio
import os
import requests
import json

TABLE_NAME_CONFIG = {
    "psychology": {
        "table_id": "<table_id>",
        "table_base": "social_content"
    },
    "book": {
        "table_id": "<table_id>",
        "table_base": "social_content"
    }
}

WORKFLOW_ID_CONFIG = {
    "gen_book_img_for_social": "<workflow_id>",
    "gen_psychology": "<gen_psychology_workflow_id>",
    "get_social_content": "<get_social_content_workflow_id>",
    "update_social_content": "<update_social_content_workflow_id>",
    "resource_category": "<resource_category_workflow_id>"
}

class PostManager:
    def __init__(self):
        pass

    async def x_send_msg(self, text=None, img_paths=None):
        chrome_manager = ChromeInstanceManager()
        driver = chrome_manager.connect_to_existing_browser()
        try:
            print(f"🌐 当前页面: {driver.current_url}")
            # Filter out non-BMP characters from the text
            if text:
                text = ''.join(char for char in text if ord(char) <= 0xFFFF)
            # Call x_post without await
            chrome_manager.x_post(text=text, img_paths=img_paths, driver=driver)
            await asyncio.sleep(3)
            # manager.close_browser()
        finally:
            # 清理资源（不关闭浏览器）
            print("发帖已结束，浏览器保持打开状态")

    async def tg_send_msg(self, text=None, img_paths=[]):
        # 替换为你的机器人token
        TOKEN = "<tg_bot_token>"
        # 替换为目标群组的chat_id
        CHAT_ID = "<chat_id>"
        tg_bot = TelegramBot(TOKEN)
        if img_paths is None or len(img_paths) == 0:
            photo_success = await tg_bot.send_message(CHAT_ID, text)
        else:
            photo_success = await tg_bot.send_multiple_photos(chat_id=CHAT_ID, photo_paths=img_paths, caption=text)
        # photo_success = await bot.send_photo_with_caption(CHAT_ID, img_path, text)
        if photo_success:
            print("电报群图文消息发送成功！")
        else:
            print("电报群图文消息发送失败！")

    def gen_psychology(self, text=None):
        if text is None:
            return None
        workflow_id = WORKFLOW_ID_CONFIG.get("gen_psychology")
        coze_manager = CozeManager(workflow_id)
        print(f"gen_psychology: {text}, ing...")
        parameters = {"topic": text}
        result, _, _ = coze_manager.run_workflow(parameters=parameters)
        print(f"Data type of result: {type(result)}")  # Print the data type of result
        try:
            if isinstance(result, str):  # Check if result is a string
                result_json = json.loads(result)  # Parse the string into a dictionary
            else:
                result_json = result  # result is already a dictionary
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            result_json = result
        print(result_json, "gen_psychology")
        img_list = result_json.get("img_list") 
        pic1 = None
        pic2 = None
        pic3 = None
        if len(img_list) > 0:
            pic1 = img_list[0]
        if len(img_list) > 1:
            pic2 = img_list[1]
        if len(img_list) > 2:
            pic3 = img_list[2]
        result_data = {
            "title": text.strip(),        
            "pic1": pic1,
            "pic2": pic2,
            "pic3": pic3,
            "content": None
        }
        return result_data

    # 调用coze工作流，生成图文消息
    def gen_book_img_for_social(self, text=None):
        if text is None:
            return None
        workflow_id = WORKFLOW_ID_CONFIG.get("gen_book_img_for_social")
        coze_manager = CozeManager(workflow_id)
        print(f"gen_book_img_for_social: {text}, ing...")
        parameters = {"input": text}
        result, _, _ = coze_manager.run_workflow(parameters=parameters)
        """
        {"content_type":1,"data":"思移力\nhttps://p26-bot-workflow-sign.byteimg.com/tos-cn-i-mdko3gqilj/b0f7d4e2d68b40538d9de5628ca34919.png~tplv-mdko3gqilj-image.png?rk3s=c8fe7ad5&x-expires=1781322820&x-signature=Dtz3dfY%2FC6sftR9iTpL92D%2BZIyc%3D\nhttps://p9-bot-workflow-sign.byteimg.com/tos-cn-i-mdko3gqilj/3441b3fbd6384195a26227d0a668508e.png~tplv-mdko3gqilj-image.png?rk3s=c8fe7ad5&x-expires=1781322818&x-signature=j%2Be24nVVEqjcuinj6WyCl7JXygo%3D\n- 📖 名称: 思移力\n- ☁️ 介绍：\n- 🔗 链接：https://pan.quark.cn/s/d672c9db71fc
    \n\n","original_result":null,"type_for_model":2}
        """
        print(f"Data type of result: {type(result)}")  # Print the data type of result
        # result是json格式，将result转换为json格式
        if isinstance(result, str):  # Check if result is a string
            result_json = json.loads(result)  # Parse the string into a dictionary
        else:
            result_json = result  # result is already a dictionary
        print(result_json, "gen_book_img_for_social")
        data = result_json.get("data")
        # 用分隔符分割data
        list = data.split("[#]")
        result_data = {
            "title": list[0],
            "pic1": list[1],
            "pic2": list[2],
            "content": list[3]
        }
        return result_data


    def download_image(self, url, file_name=None, save_dir="downloads"):
        """
        下载图片并返回本地路径。
        :param url: 图片的URL地址
        :param save_dir: 保存图片的目录，默认为 "downloads"
        :return: 本地图片路径
        """
        # 确保保存目录存在
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        if url.startswith("http") is False:
            return None
        # 从URL中提取文件名
        if file_name is None:
            file_name = os.path.basename(url)
        local_path = os.path.join(save_dir, file_name)

        print("图片下载:", url)
        # 下载图片
        response = requests.get(url)
        if response.status_code == 200:
            with open(local_path, 'wb') as file:
                file.write(response.content)
            return local_path
        else:
            raise Exception(f"图片下载失败，状态码: {response.status_code}")

    async def post(self, json_data):
        if json_data is None:
            return None
        title = json_data.get("title")
        pic1 = json_data.get("pic1")
        pic2 = json_data.get("pic2")
        pic3 = json_data.get("pic3")
        content = json_data.get("content")
        if content is None or len(content) == 0:
            print("描述为空，不允许发布到社交平台")
            return

        save_dir = "E:/迅雷下载/douyin/py/download"

        random_number = random.randint(1, 1000000)  # 生成一个随机数
        img_paths = []
        if pic1 is not None and len(pic1) > 0:
            pic1_name = title + str(random_number) + "pic1.png"
            pic1_path = self.download_image(pic1, pic1_name, save_dir)
            if pic1_path is not None:
                img_paths.append(pic1_path)
        if pic2 is not None and len(pic2) > 0:
            pic2_name = title + str(random_number) + "pic2.png"
            pic2_path = self.download_image(pic2, pic2_name, save_dir)
            if pic2_path is not None:
                img_paths.append(pic2_path)
        if pic3 is not None and len(pic3) > 0:
            pic3_name = title + str(random_number) + "pic3.png"
            pic3_path = self.download_image(pic3, pic3_name, save_dir)
            if pic3_path is not None:
                img_paths.append(pic3_path)
        send_content = ""
        if content is not None:
            send_content = content
        else:
            send_content = title
        await self.tg_send_msg(text=send_content, img_paths=img_paths)
        # await self.x_send_msg(text=send_content, img_paths=img_paths)

if __name__ == "__main__":
    post_manager = PostManager()
    while True:
        # 获取输入的值，将值传递给coze_wf_send
        one = input("请输入1.心理学 2.书籍：")
        if one == "1":
            name = input("请输入心理学主题:")
            print("【心理学】", name)
            json_data = post_manager.gen_psychology(name)
            asyncio.run(post_manager.post(json_data))
        elif one == "2":
            name = input("请输入书名:")
            # # 1、调用工作流，生成图片和资源内容
            print("【书籍】", name)
            json_data = post_manager.gen_book_img_for_social(name)
            asyncio.run(post_manager.post(json_data))
        else:
            print("输入错误")
            continue
    