import sys

sys.path.append(".")

from pydantic import ValidationError
from module.commons.stock.stock import SessionLocal, engine, Base
from module.commons.datatype.daily_k import (
    insert_daily_k,
    get_daily_k,
)
from module.crawler.daily_k import fetch_stock_data


def daily_k_db():
    db = SessionLocal()
    try:
        # 创建数据库表
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"An error occurred while creating database tables: {e}")

    # 抓取数据并标准化
    daily_k_data_list = fetch_stock_data()
    for data_dict in daily_k_data_list:
        try:
            # 标准化数据
            # 插入数据到数据库
            insert_daily_k(db, data_dict)
        except ValidationError as e:
            print(f"Data validation error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    # 查询并打印数据（可选）
    stock_data = get_daily_k(db, "sh.600000")
    print(stock_data)
    print(type(stock_data))
    if stock_data:
        print(
            f"Date: {stock_data.date}, Open: {stock_data.open}, High: {stock_data.high}, Low: {stock_data.low}, Close: {stock_data.close}, Volume: {stock_data.volume}, Amount: {stock_data.amount}"
        )

    db.close()
