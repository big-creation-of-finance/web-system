from .daily_k import fetch_stock_data
import time
import schedule


def cron():
    # 安排任务每天运行一次，可以设置具体时间，例如每天的9:00
    schedule.every().day.at("05:00").do(fetch_stock_data)

    # 持续运行调度器
    while True:
        schedule.run_pending()
        time.sleep(1)
