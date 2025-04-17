import yaml
import requests
import time
import certifi
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / 'config' / 'config.yml'
LOG_DIR = Path(__file__).parent / 'logs'

RETRY_COUNT = 3
RETRY_DELAY = 5
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json'
}

def load_config():
    with open(CONFIG_PATH, 'r') as f:
        config = yaml.safe_load(f)
    return config.get('urls', [])

def poll_urls():
    urls = load_config()
    LOG_DIR.mkdir(exist_ok=True)
    
    log_file = LOG_DIR / f'poll_urls_{int(time.time())}.log'
    
    for url in urls:
        success = False
        for attempt in range(RETRY_COUNT):
            try:
                response = requests.get(url, headers=HEADERS, timeout=10, verify=certifi.where())
                status = '成功' if response.ok else '失败'
                log = f"[{time.ctime()}] {url} {status} 状态码:{response.status_code} 尝试:{attempt+1}"
                print(log)
                
                with open(log_file, 'a') as f:
                    f.write(log + '\n')
                
                if response.ok:
                    success = True
                    break
                
            except Exception as e:
                log = f"[{time.ctime()}] {url} 异常: {str(e)} 尝试:{attempt+1}"
                print(log)
                with open(log_file, 'a') as f:
                    f.write(log + '\n')
                
            time.sleep(RETRY_DELAY)
        
        if not success:
            print(f"[{time.ctime()}] {url} 所有重试均失败")
            with open(log_file, 'a') as f:
                f.write(f"[{time.ctime()}] {url} 所有重试均失败\n")

if __name__ == '__main__':
    poll_urls()