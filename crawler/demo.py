import time
from data import AllData


def writer():
    # 只是模拟爬虫将数据写入的操作
    # 将（爬取的）数据写入数据库
    written_data = 1
    while 1:
        written_data += 1
        AllData.write(written_data)
        print(written_data)  # 调试用
        time.sleep(1)
