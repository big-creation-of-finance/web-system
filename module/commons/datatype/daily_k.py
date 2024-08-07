from datetime import datetime, timedelta


import pytz
import holidays
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, REAL
from sqlalchemy.orm import Session

from ..stock.stock import Base


class daily_k_StockData(BaseModel):
    date: str
    code: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    amount: float
    # 可以继续添加其他字段

    class Config:
        orm_mode = True


class dailyk(Base):
    __tablename__ = "dailyk"

    # 关系型数据库需要一个主键
    id = Column(Integer, primary_key=True)

    date = Column(Integer, index=True)
    code = Column(String, index=True)
    open = Column(REAL)
    high = Column(REAL)
    low = Column(REAL)
    close = Column(REAL)
    volume = Column(Integer)
    amount = Column(REAL)


# 转换函数：daily_k_StockData 转换为 dailyk
def daily_k_StockData_to_dailyk(data: daily_k_StockData) -> dailyk:
    return dailyk(
        date=str_to_utc8_timestamp(data.date),
        code=data.code,
        open=data.open,
        high=data.high,
        low=data.low,
        close=data.close,
        volume=data.volume,
        amount=data.amount,
    )


# 转换字符串日期到UTC+8时间戳的辅助函数
def str_to_utc8_timestamp(date: str) -> int:
    # 将字符串转换为datetime对象
    dt = datetime.strptime(date, "%Y-%m-%d")
    # 获取北京时间的时间戳
    return int(dt.timestamp())


# 辅助函数，获取当前日期零点UTC+8的时间戳
def get_current_midnight_utc8_timestamp():
    now = datetime.now()
    # 将当前时间转换为UTC+8时区
    utc8_tz = pytz.timezone("Asia/Shanghai")
    now_utc8 = now.astimezone(utc8_tz)
    # 获取当前日期零点UTC+8的时间戳，并转换为datetime对象
    midnight_utc8 = now_utc8.replace(hour=0, minute=0, second=0, microsecond=0)
    # 将midnight_utc8设置为下一天的零点
    next_midnight_utc8 = midnight_utc8 + timedelta(days=1)
    return int(next_midnight_utc8.timestamp())


# 创建一个中国节假日的实例
def is_weekend_or_holiday(date: datetime.date) -> bool:
    # 判断给定日期是否是周末或者法定节假日
    chn_holidays = holidays.CN()
    return date.weekday() >= 5 or date in chn_holidays


def check_data_integrity(db: Session, stock_code: str) -> list:
    missing_dates = []
    start_date_str = "2024-07-01"
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_timestamp = get_current_midnight_utc8_timestamp()
    end_date = datetime.fromtimestamp(
        end_timestamp, tz=pytz.timezone("Asia/Shanghai")
    ).date()

    # 获取数据库中所有该股票代码的数据
    all_data = (
        db.query(dailyk)
        .filter(
            dailyk.code == stock_code,
            dailyk.date >= str_to_utc8_timestamp(start_date_str),
            dailyk.date <= end_timestamp,  # 使用 <= 确保包含结束日期的数据
        )
        .all()
    )

    # 创建一个集合，包含数据库中所有数据的日期
    existing_dates = {
        datetime.fromtimestamp(item.date, tz=pytz.timezone("Asia/Shanghai")).date()
        for item in all_data
    }

    # 检查从start_date到end_date的每一天是否都有数据
    current_date = start_date
    while current_date <= end_date:
        if not is_weekend_or_holiday(current_date):
            # 检查当前日期是否存在于数据库中已有数据的日期集合中
            if current_date not in existing_dates:
                missing_dates.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)

    return sorted(missing_dates)  # 返回排序后的缺失日期列表


# def get_daily_k(db: Session, code: str) -> dailyk | None:
#     return db.query(dailyk).filter(dailyk.code == code).first()


# def insert_daily_k(db: Session, data: daily_k_StockData) -> dailyk:
#     db_user = dailyk(
#         **data.dict(exclude={"date"}), date=str_to_utc8_timestamp(data.date)
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
