import baostock as bs
from pydantic import ValidationError
import time


from module.commons.stock.stock import SessionLocal, engine, Base
from module.commons.datatype.daily_k import (
    daily_k_StockData,
    daily_k_StockData_to_dailyk,
    check_data_integrity,
)


def fetch_stock_data(stock_codes, start_date, end_date):

    stock_data_list = []
    for code in stock_codes:
        daily_k_data = _get_daily_k_data(code, start_date, end_date)
        if daily_k_data:
            stock_data_list.extend(daily_k_data)

    return stock_data_list


def _get_daily_k_data(code, start_date, end_date):
    # _开头的变量意为不导出

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

    return stock_data_list


def daily_k_db():
    time1 = time.time()
    db = SessionLocal()
    daily_k_objects = []

    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"An error occurred while creating database tables: {e}")

    stock_codes = [
        "sh.600000",
        # "sz.000001",
        # "sz.000651",
        # "sh.600690",
    ]

    lg = bs.login()
    if lg.error_code != "0":
        return None

    for stock_code in stock_codes:
        # 检查并补全数据
        missing_dates = check_data_integrity(db, stock_code)
        for missing_date in missing_dates:
            daily_k_data = fetch_stock_data(
                [stock_code],
                missing_date,
                missing_date,
            )

            for data in daily_k_data:
                try:
                    db_entry = daily_k_StockData_to_dailyk(data)
                    daily_k_objects.append(db_entry)
                except ValidationError as e:
                    print(f"Data validation error for {stock_code}: {e}")

    # 所有数据收集完毕后，一次性插入数据库
    try:
        db.add_all(daily_k_objects)
        db.commit()
        print("Data insertion completed successfully.")
    except Exception as e:
        print(f"An error occurred while inserting data: {e}")
    finally:
        # Baostock 登出
        bs.logout()
        # 关闭数据库会话
        db.close()

    time2 = time.time()
    execution_time = time2 - time1
    print(f"代码执行时间：{execution_time}秒")
