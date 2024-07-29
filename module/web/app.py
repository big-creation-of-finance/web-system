import uvicorn
from fastapi import Depends, FastAPI, HTTPException, FastAPI
from sqlalchemy.orm import Session

from ..commons.datatype.daily_k import daily_k_StockData, get_daily_k
from ..commons.stock.stock import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/company/{code}/dailyk", response_model=daily_k_StockData)
async def daily_k(code: str, db: Session = Depends(get_db)):
    db_daily_k = get_daily_k(db, code)
    if db_daily_k:
        return db_daily_k
    raise HTTPException(status_code=404, detail='Not Found')


def run():
    uvicorn.run(app, host="0.0.0.0", port=8000)
