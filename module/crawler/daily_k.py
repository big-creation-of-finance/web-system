# daily_k.py
# from dataclasses import dataclass
from datetime import datetime

import baostock as bs

from ..commons.datatype import daily_k_StockData


def get_daily_k_data(code, start_date, end_date):
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
