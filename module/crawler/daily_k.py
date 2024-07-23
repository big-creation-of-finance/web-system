from datetime import datetime, timedelta

import baostock as bs

from ..commons.datatype import daily_k_StockData


def fetch_stock_data():
    # 获取当前日期
    end_date = datetime.now().strftime("%Y-%m-%d")
    # 计算90天前的日期，观察到日k线大概90天左右
    start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")

    stock_code = "sh.600000"

    # 输入股票代码，开始时间，结束时间引用
    daily_k_data = _get_daily_k_data(stock_code, start_date, end_date)
    if daily_k_data is not None:
        for stock in daily_k_data:
            print(stock.date, stock.code, stock.open, stock.low)
    else:
        print("No stock data available.")


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
