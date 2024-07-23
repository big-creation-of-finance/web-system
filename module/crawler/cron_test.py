import sys
sys.path.append(".")


if __name__ == "__main__":
    # 在此处测试每个定时任务
    from module.crawler.daily_k import fetch_stock_data
    fetch_stock_data()
