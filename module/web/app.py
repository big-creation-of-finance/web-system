from datetime import date

from fastapi import FastAPI
import uvicorn

from ..commons.datatype import daily_k_StockData

app = FastAPI()


# 简易 web app 演示，返回数据库中一个数据
# @app.get("/")
# async def root():
#     show_data = AllData.read()
#     return {"message": show_data}


@app.get("/company/{code}/dailyk")
async def daily_k(start: date, end: date) -> list[daily_k_StockData]:

    return


def run():
    uvicorn.run(app, host="0.0.0.0", port=8000)
