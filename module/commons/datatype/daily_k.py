from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, REAL
from sqlalchemy.orm import Session

from ..stock.stock import Base


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

    class Config:
        orm_mode = True


class dailyk(Base):
    __tablename__ = "dailyk"

    # 关系型数据库需要一个主键
    id = Column(Integer, primary_key=True)

    date = Column(String, index=True)
    code = Column(String, index=True)
    open = Column(REAL)
    high = Column(REAL)
    low = Column(REAL)
    close = Column(REAL)
    volume = Column(Integer)
    amount = Column(REAL)


def get_daily_k(db: Session, code: str) -> dailyk | None:
    return db.query(dailyk).filter(dailyk.code == code).first()


# def insert_daily_k(db: Session, data: daily_k_StockData) -> dailyk:
#     db_user = dailyk(**data.dict(exclude={"date"}), date=str(data.date))
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


def insert_daily_k(db: Session, data: daily_k_StockData) -> dailyk | None:
    # 检查数据库中是否已经存在该记录
    existing_record = (
        db.query(dailyk)
        .filter(
            dailyk.date == str(data.date),  # 确保date是字符串形式
            dailyk.code == data.code,
        )
        .first()
    )

    if existing_record:
        return None

    # 如果记录不存在，则创建新记录并插入数据库
    db_user = dailyk(**data.dict(exclude={"date"}), date=str(data.date))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
