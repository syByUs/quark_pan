import os
import json
import random
import psutil
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 配置文件路径
CONFIG_FILE = "E:/迅雷下载/douyin/py/browser_config.json"
USER_DATA_DIR = "E:/chrome_user_data"

class ChromeInstanceManager:
    def __init__(self):
        # 创建用户数据目录（如果不存在）
        os.makedirs(USER_DATA_DIR, exist_ok=True)
        self.config = self.load_config()
        
    def load_config(self):
        """加载或创建配置文件"""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        else:
            return {"debug_port": 9222, "browser_pid": None, "window_handles": []}
    
    def save_config(self):
        """保存配置文件"""
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def is_browser_running(self):
        """检查浏览器是否在运行"""
        print(f"检查浏览器是否在运行1: {self.config['browser_pid']}")
        if self.config["browser_pid"] is None:
            return False
        
        try:
            process = psutil.Process(self.config["browser_pid"])
            print(f"检查浏览器是否在运行2: {process.is_running()}, {process.name()}")
            return process.is_running() and process.name() == "chrome.exe"
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return False
    
    def start_chrome(self):
        """启动 Chrome 浏览器并配置远程调试"""
        # 构造 Chrome 启动命令
        chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"  # 修改为你的 Chrome 路径
        chrome_cmd = [
            chrome_path,
            "--remote-debugging-port=8633",
            f"--user-data-dir={USER_DATA_DIR}",
            f"--remote-debugging-port={self.config['debug_port']}",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-infobars",
            "--disable-blink-features=AutomationControlled",
            "useAutomationExtension=false",
            "https://x.com/home"  # 启动时打开的页面
        ]
        
        # 启动 Chrome 进程
        process = subprocess.Popen(chrome_cmd)
        
        # 保存进程信息
        self.config["browser_pid"] = process.pid
        self.save_config()
        
        # print(f"✅ 已启动新 Chrome 实例，PID: {process.pid}, {self.config["browser_pid"]}")
        return process.pid
    
    def connect_to_existing_browser(self):
        """连接到已运行的 Chrome 实例"""
        if not self.is_browser_running():
            print("⚠️ 没有运行的 Chrome 实例，正在启动新实例...")
            self.start_chrome()
            time.sleep(8)  # 等待浏览器启动
        
        # 配置 Selenium 连接到现有浏览器
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{self.config['debug_port']}")
        
        # 初始化 WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        
        # 获取当前所有标签页
        current_tabs = driver.window_handles
        
        # 检查是否有 x.com/home 标签页
        x_tab = None
        for tab in current_tabs:
            driver.switch_to.window(tab)
            if driver.current_url == "https://x.com/home":
                x_tab = tab
                break
        
        # 如果没有 x.com/home 标签页，创建新标签页
        if not x_tab:
            print("➡️ 创建新的 x.com/home 标签页")
            driver.execute_script("window.open('https://x.com/home');")
            driver.switch_to.window(driver.window_handles[-1])
            x_tab = driver.current_window_handle
        else:
            print(f"🔍 找到 x.com/home 标签页: {x_tab}")
            driver.switch_to.window(x_tab)
        
        # 更新窗口句柄配置
        self.config["window_handles"] = current_tabs
        self.save_config()
        
        return driver
    
    def close_browser(self):
        """关闭浏览器（可选）"""
        if self.is_browser_running():
            try:
                pid = self.config["browser_pid"]
                print(f"待关闭的pid: {pid}")
                process = psutil.Process(pid)
                process.terminate()
                print(f"🛑 已关闭 Chrome 实例，PID: {pid}")
                self.config["browser_pid"] = None
                self.save_config()
            except Exception as e:
                print(f"关闭浏览器时出错: {e}")
        else:
            print("浏览器没有运行")
    def x_input(self, text, driver):        
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div")))
            input = driver.find_element(by=By.XPATH, value="//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div")
            input.send_keys(text)
            time.sleep(1)
        except Exception as e:
            print("exception:", e)
    def x_input_img(self, img_path, driver):
        try:
            x_path = "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/nav/div/div[2]/div/div[1]/div/input"
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, x_path)))
            input = driver.find_element(by=By.XPATH, value=x_path)
            input.send_keys(img_path)
            time.sleep(1)
            WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-testid='attachments']")))
            print("图片上传中...") 
        except Exception as e:
            print("exception:", e)
    def x_post(self, text=None, img_paths=None, driver=None):
        if driver is None:
            return
        if text is None and img_paths is None:
            return
        random_number = random.randint(1000, 5000)
        if text is not None:
            self.x_input(text, driver)
        if img_paths is not None:
            for img_path in img_paths:
                file_size = os.path.getsize(img_path)
                upload_speed = 1000 * 1024  # 500 KB/s
                upload_time = file_size / upload_speed
                random_number = upload_time * 1000
                print(f"上传时间: {upload_time:.2f} 秒")
                self.x_input_img(img_path, driver)
                n = random_number / 1000.0
                time.sleep(max(n, 2))
        self.x_post_only(driver)
    def x_post_only(self, driver=None):
        x_path = "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/button"
        while True:
            try:
                print("等待元素出现")
                time.sleep(2)
                WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.XPATH, x_path)))
                WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.XPATH, x_path)))
                post = driver.find_element(by=By.XPATH, value=x_path)
                post.click()
                print("post x out")
                break
            except Exception as e:
                print("post exception:", e)
# 使用示例
if __name__ == "__main__":
    manager = ChromeInstanceManager()
    
    # 连接到现有浏览器或启动新实例
    driver = manager.connect_to_existing_browser()
    if driver is None:
        print("driver is None")
        exit()
    
    try:
        # 执行 x 操作
        print(f"🌐 当前页面: {driver.current_url}")
        
        # 在此处添加你的 x 操作代码
        # 例如：发布推文、浏览时间线等
        # manager.x_post("Hello, world! test selenium")
        # manager.x_input("beef不只是牛肉你知道它还有这些意思吗")
        img2 = "E:/迅雷下载/douyin/上苍之上/new/221-上苍世界221集荒天帝石昊大战黑暗帝皇上.mp4"
        # manager.x_input_img(img2)
        manager.x_post(text="让我试一试通过selenium发帖好不好使，哈哈哈", img_path=None, driver=driver)

        # 示例：等待用户操作
        input("按回车键结束程序（浏览器将保持打开）...")
        manager.close_browser()
    finally:
        # 清理资源（不关闭浏览器）
        driver.quit()
        print("程序已结束，浏览器保持打开状态")
