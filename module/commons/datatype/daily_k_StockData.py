# common/datatype/stock_data.py
# from dataclasses import dataclass
from pydantic import BaseModel
from datetime import datetime


# @dataclass
class daily_k_StockData(BaseModel):
    date: datetime
    code: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    amount: float
    # 可以继续添加其他字段
