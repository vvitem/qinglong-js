"""
脚本名称: poll_urls.py
功能: 定时监测多个URL的健康状态，支持分组轮询和重试机制

环境变量:
POLL_URLS - URL组配置，格式：组1URL1&组1URL2@组2URL1 (用@分隔组，&分隔同组URL)
示例: export POLL_URLS="http://api1.example.com&http://api2.example.com@http://monitor.example.com"

依赖库:
- requests
- certifi
- python-dotenv (可选，用于环境变量文件加载)

执行方式:
python poll_urls.py

日志存储:
./logs/poll_urls_<timestamp>.log

异常处理:
- 网络异常自动重试3次
- 所有重试失败后记录错误日志
"""
import os
import time
import certifi
import requests
import logging

class UrlPoller:
    def __init__(self, urls):
        self.urls = urls
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }

    def poll_single(self, url):
        success = False
        for attempt in range(3):
            try:
                response = requests.get(url, headers=self.headers, timeout=10, verify=certifi.where())
                status = '成功' if response.ok else '失败'
                log_msg = f"[{time.ctime()}] {url} {status} 状态码:{response.status_code} 尝试:{attempt+1}"
                if response.ok:
                    logging.info(log_msg)
                    success = True
                    break
                else:
                    logging.error(log_msg)
            except Exception as e:
                log_msg = f"[{time.ctime()}] {url} 异常: {str(e)} 尝试:{attempt+1}"
                logging.error(log_msg)
            time.sleep(5)
        if not success:
            logging.error(f"[{time.ctime()}] {url} 所有重试均失败")

    def poll_all(self):
        for url in self.urls:
            print(f"=====开始监测URL: {url}=====")
            self.poll_single(url)
            print("---------监测完成---------")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] ===> %(message)s')
    poll_urls = os.environ.get('POLL_URLS')
    if not poll_urls:
        print("请设置环境变量 'POLL_URLS' (多个URL用@分割)")
    else:
        url_groups = poll_urls.split('@')
        for num, urls in enumerate(url_groups, start=1):
            print(f"=====开始执行第{num}组URL任务=====")
            poller = UrlPoller(urls.split('&'))
            poller.poll_all()
            print("---------任务执行完毕---------")