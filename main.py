import time
from threading import Thread

from .web import run as webapp
from .crawler import main


def main():
    # 简易模块划分的demo，并不完全
    threads = [
        Thread(target=webapp, daemon=True),  # webapp的线程
        Thread(target=main, daemon=True)]  # 爬虫的线程（之后应该改为定时器触发）
    for thread in threads:
        thread.start()
    while 1:
        time.sleep(1)


if __name__ == '__main__':
    main()
