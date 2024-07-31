import sys

sys.path.append(".")


if __name__ == "__main__":
    # 在此处测试每个定时任务
    from module.crawler.daily_k_test import daily_k_db

    daily_k_db()
