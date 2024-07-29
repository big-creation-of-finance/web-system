import sys
from datetime import datetime
sys.path.append('.')


def daily_test():
    from module.commons.stock.stock import SessionLocal, engine, Base
    from module.commons.datatype.daily_k import insert_daily_k, daily_k_StockData, get_daily_k
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # 生成一条记录
    data = daily_k_StockData(
        date=datetime.now(),
        code=114514,
        open=1.21,
        high=1.30,
        low=1.19,
        close=1.20,
        volume=1,
        amount=1.2
    )
    # 插入数据库
    insert_daily_k(db=db, data=data)

    # 查询数据
    return_data = get_daily_k(db=db, code=114514)
    print(return_data.date)
    print(return_data.code)
    print(return_data.open)


if __name__ == '__main__':
    daily_test()
