from django.apps import AppConfig
import threading
import time
import random
import requests
import logging
from django.apps import AppConfig

logger = logging.getLogger(__name__)

class PingService:
    def __init__(self, url, min_interval=5, max_interval=14):
        """
        初始化自我ping服务
        
        :param url: 要ping的URL
        :param min_interval: 最小间隔时间(分钟)
        :param max_interval: 最大间隔时间(分钟)
        """
        self.url = url
        self.min_interval = min_interval  # 分钟
        self.max_interval = max_interval  # 分钟
        self.is_running = False
        self.thread = None
    
    def start(self):
        """启动ping服务"""
        if self.is_running:
            return
        
        self.is_running = True
        self.thread = threading.Thread(target=self._ping_loop)
        self.thread.daemon = True  # 设为守护线程，这样当主程序退出时，此线程也会退出
        self.thread.start()
        logger.info(f"Ping服务已启动，将ping {self.url}，间隔为{self.min_interval}-{self.max_interval}分钟")
    
    def stop(self):
        """停止ping服务"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=1)
        logger.info("Ping服务已停止")
    
    def _ping_loop(self):
        """ping循环逻辑"""
        while self.is_running:
            try:
                # 随机等待时间(分钟)，转换为秒
                wait_time = random.randint(self.min_interval, self.max_interval) * 60
                time.sleep(wait_time)
                
                # 发送请求
                response = requests.get(self.url, timeout=10)
                logger.info(f"Ping {self.url}: 状态码 {response.status_code}")
            except Exception as e:
                logger.error(f"Ping失败: {str(e)}")

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'  # 替换为你的应用名称
    
    def ready(self):
        """当Django应用准备就绪时调用"""
        # 确保不是在Django管理命令(如migrate)中运行
        import sys
        if 'runserver' in sys.argv or 'gunicorn' in sys.argv[0] or 'uvicorn' in sys.argv[0]:
            # 应用URL，替换为你的实际URL
            app_url = 'https://anti-memo-frontend-test-11-20-2024.onrender.com/login'
            app_url2 = 'https://anti-memo-frontend-test-11-20-2024.onrender.com/login'
            
            # 创建并启动ping服务
            ping_service = PingService(url=app_url, min_interval=5, max_interval=14)
            ping_service.start()
            
            # 创建并启动ping服务
            ping_service2 = PingService(url=app_url2, min_interval=5, max_interval=14)
            ping_service2.start()




# 在apps.py中使用上述代码
# 然后在__init__.py中添加:
# default_app_config = 'myapp.apps.MyAppConfig'  # 替换'myapp'为你的应用名称