import logging
from telegram import Bot, InputMediaPhoto
from telegram.error import TelegramError
import asyncio
import os

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self, token):
        self.bot = Bot(token=token)
        
    async def send_message(self, chat_id, text):
        """
        发送消息到指定的聊天
        
        Args:
            chat_id (str): 聊天ID（群组ID或用户ID）
            text (str): 要发送的消息内容
            
        Returns:
            bool: 发送是否成功
        """
        try:
            await self.bot.send_message(chat_id=chat_id, text=text)
            logger.info(f"消息已成功发送到 {chat_id}")
            return True
        except TelegramError as e:
            logger.error(f"发送消息时出错: {e}")
            return False

    async def send_photo_with_caption(self, chat_id, photo_path, caption=None):
        """
        发送带说明文字的图片消息
        
        Args:
            chat_id (str): 聊天ID（群组ID或用户ID）
            photo_path (str): 图片文件的路径
            caption (str, optional): 图片说明文字
            
        Returns:
            bool: 发送是否成功
        """
        try:
            if not os.path.exists(photo_path):
                logger.error(f"图片文件不存在: {photo_path}")
                return False
                
            with open(photo_path, 'rb') as photo:
                await self.bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=caption
                )
            logger.info(f"图片消息已成功发送到 {chat_id}")
            return True
        except TelegramError as e:
            logger.error(f"发送图片消息时出错: {e}")
            return False
        except Exception as e:
            logger.error(f"处理图片时出错: {e}")
            return False

    async def send_multiple_photos(self, chat_id, photo_paths, caption=None):
        """
        发送多张图片作为相册
        
        Args:
            chat_id (str): 聊天ID（群组ID或用户ID）
            photo_paths (list): 图片文件路径的列表
            caption (str, optional): 相册的说明文字（仅第一张图片显示）
            
        Returns:
            bool: 发送是否成功
        """
        try:
            media_group = []
            for i, photo_path in enumerate(photo_paths):
                if not os.path.exists(photo_path):
                    logger.error(f"图片文件不存在: {photo_path}")
                    continue
                
                with open(photo_path, 'rb') as photo:
                    media_group.append(
                        InputMediaPhoto(media=photo, caption=caption if i == 0 else None)
                    )
            
            if not media_group:
                logger.error("没有有效的图片文件")
                return False
                
            await self.bot.send_media_group(chat_id=chat_id, media=media_group)
            logger.info(f"多张图片已成功发送到 {chat_id}")
            return True
        except TelegramError as e:
            logger.error(f"发送多张图片时出错: {e}")
            return False
        except Exception as e:
            logger.error(f"处理多张图片时出错: {e}")
            return False

async def main():
    # 替换为你的机器人token
    TOKEN = "7337007704:AAGktemkMXY37YMgDCAcabppG7NEZr4gzT8"
    # 替换为目标群组的chat_id
    CHAT_ID = "-1002775900045"
    
    bot = TelegramBot(TOKEN)
    
    # 发送多张图片
    photo_paths = [
        "E:/迅雷下载/douyin/py/download/贪婪的多巴胺pic1.png",  # 替换为实际的图片路径
        "E:/迅雷下载/douyin/py/download/心理学与生活pic1.png"  # 替换为实际的图片路径
    ]
    caption = "这是一组测试图片"
    success = await bot.send_multiple_photos(CHAT_ID, photo_paths, caption)
    
    if success:
        print("多张图片消息发送成功！")
    else:
        print("多张图片消息发送失败！")

if __name__ == "__main__":
    asyncio.run(main())
