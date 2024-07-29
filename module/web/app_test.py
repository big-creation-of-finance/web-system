import sys
sys.path.append('.')

if __name__ == '__main__':
    from module.web.app import daily_k
    from module.commons.stock.stock import SessionLocal, engine, Base
    # from commons.datatype.daily_k_StockData import Base
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    print(daily_k(1, db))
