import sqlite3
import sys
sys.path.append('.')


if __name__ == '__main__':
    from module.commons.stock import create_table_from_dataclass
    from module.commons.datatype import daily_k_StockData
    con = sqlite3.connect("data_test.db")
    create_table_from_dataclass(conn=con, dataclass_type=daily_k_StockData)
