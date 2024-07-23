# main.py
from .daily_k import get_daily_k_data


def main():
    # stock_code = input("Enter the stock code (e.g., 'sh.600000'): ")
    # start_date = input("Enter the start date (YYYY-MM-DD): ")
    # end_date = input("Enter the end date (YYYY-MM-DD): ")

    stock_code = "sh.600000"
    start_date = "2024-01-30"
    end_date = "2024-02-05"

    # 输入股票代码，开始时间，结束时间引用
    daily_k_data = get_daily_k_data(stock_code, start_date, end_date)
    if daily_k_data is not None:
        for stock in daily_k_data:
            print(
                f"Date: {stock.date}, Code: {stock.code}, Open: {
                    stock.open}, Low: {stock.low}"
            )
    else:
        print("No stock data available.")


if __name__ == "__main__":
    main()
