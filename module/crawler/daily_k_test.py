import time


import baostock as bs
from pydantic import ValidationError


from module.commons.stock.stock import SessionLocal, engine, Base
from module.commons.datatype.daily_k import daily_k_StockData
from module.commons.datatype.daily_k import daily_k_StockData_to_dailyk


def fetch_stock_data(stock_codes):

    # 获取当前日期
    end_date = "2024-07-26"
    start_date = "2016-01-01"
    stock_data_list = []
    for code in stock_codes:
        daily_k_data = _get_daily_k_data(code, start_date, end_date)
        if daily_k_data:
            stock_data_list.extend(daily_k_data)

    return stock_data_list


def _get_daily_k_data(code, start_date, end_date):
    # _开头的变量意为不导出
    lg = bs.login()
    if lg.error_code != "0":
        return None

    # 请将date写在第一个
    rs = bs.query_history_k_data_plus(
        code,
        "date,code,open,high,low,close,volume,amount",
        start_date=start_date,
        end_date=end_date,
        frequency="d",
        adjustflag="3",
    )

    stock_data_list = []

    if rs is None or rs.error_code != "0":
        print("Failed to get stock data result set or error in result set.")
        bs.logout()
        return None

    # 获取字段名
    while rs.next():
        record = rs.get_row_data()

        stock_data_kwargs = {
            "date": record[0],
            "code": record[1],
            "open": float(record[2]),
            "high": float(record[3]),  # 显式转换为 float
            "low": float(record[4]),
            "close": float(record[5]),
            "volume": int(record[6]),
            "amount": float(record[7]),
        }
        stock_data = daily_k_StockData(**stock_data_kwargs)
        stock_data_list.append(stock_data)

    bs.logout()
    return stock_data_list


def daily_k_db_quick():
    start_time1 = time.time()
    db = SessionLocal()
    try:
        # 创建数据库表
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"An error occurred while creating database tables: {e}")
    stock_codes = [
        "sh.600000",
    ]  # 示例股票代码列表
    # 抓取数据并标准化
    daily_k_data_list = fetch_stock_data(stock_codes)
    end_time1 = time.time()
    execution_time = end_time1 - start_time1
    print(f"代码执行时间：{execution_time}秒")
    print("done with stock")

    start_time2 = time.time()
    # 收集所有数据对象
    daily_k_objects = []
    for data_dict in daily_k_data_list:
        try:
            db_entry = daily_k_StockData_to_dailyk(data_dict)
            daily_k_objects.append(db_entry)
        except ValidationError as e:
            print(f"Data validation error: {e}")

    # 一次性插入所有数据
    try:
        db.add_all(daily_k_objects)
        db.commit()
    except Exception as e:
        print(f"An error occurred while inserting data: {e}")
    finally:
        db.close()

    end_time2 = time.time()
    execution_time = end_time2 - start_time2
    print(f"shujuku代码执行时间：{execution_time}秒")
    print("done with insert")

