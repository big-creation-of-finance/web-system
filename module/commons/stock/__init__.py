import sqlite3

from ..datatype.daily_k_StockData import daily_k_StockData
from .stock import create_table_from_dataclass

con = sqlite3.connect("data.db")
create_table_from_dataclass(conn=con, dataclass_type=daily_k_StockData)

__all__ = [con]
