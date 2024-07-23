# common/datatype/stock_data.py
from dataclasses import dataclass
from datetime import datetime


@dataclass
class daliy_k_StockData:
    date: datetime
    code: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    amount: float
    # 可以继续添加其他字段
