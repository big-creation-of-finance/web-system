import sys
import time
from datetime import datetime, timedelta
import schedule

# 添加你的模块路径
sys.path.append(".")

# 导入你自己的模块
from module.crawler import get_daily_k_data


def fetch_stock_data():
    # 获取当前日期
    end_date = datetime.now().strftime("%Y-%m-%d")
    # 计算90天前的日期，观察到日k线大概90天左右
    start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")

    stock_code = "sh.600000"

    # 输入股票代码，开始时间，结束时间引用
    daily_k_data = get_daily_k_data(stock_code, start_date, end_date)
    if daily_k_data is not None:
        for stock in daily_k_data:
            print(stock.date, stock.code, stock.open, stock.low)
    else:
        print("No stock data available.")


if __name__ == "__main__":
    # 安排任务每天运行一次，可以设置具体时间，例如每天的9:00
    schedule.every().day.at("05:00").do(fetch_stock_data)

    # 持续运行调度器
    while True:
        schedule.run_pending()
        time.sleep(1)
