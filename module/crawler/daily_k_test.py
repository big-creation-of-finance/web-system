from datetime import datetime, timedelta


import baostock as bs
from pydantic import ValidationError


from module.commons.stock.stock import SessionLocal, engine, Base
from module.commons.datatype.daily_k import daily_k_StockData
from module.commons.datatype.daily_k import insert_daily_k


def fetch_stock_data(stock_codes):

    # 获取当前日期
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = "2016-01-30"
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
        date_str = record[0]
        date_dt = datetime.strptime(date_str, "%Y-%m-%d")
        stock_data_kwargs = {
            "date": date_dt,
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


def daily_k_db():
    db = SessionLocal()
    try:
        # 创建数据库表
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"An error occurred while creating database tables: {e}")
    stock_codes = [
        "sh.600000",
        "sz.000001",
        "sz.000651",
        "sh.600690",
    ]  # 示例股票代码列表
    # 抓取数据并标准化
    daily_k_data_list = fetch_stock_data(stock_codes)

    for data_dict in daily_k_data_list:
        try:
            # 标准化数据
            # 插入数据到数据库
            insert_daily_k(db, data_dict)
        except ValidationError as e:
            print(f"Data validation error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    db.close()
