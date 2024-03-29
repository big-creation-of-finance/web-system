from fastapi import FastAPI
import uvicorn

from data import AllData

app = FastAPI()


# 简易 web app 演示，返回数据库中一个数据
@app.get("/")
async def root():
    show_data=AllData.read()
    return {"message": show_data}

def run():
    uvicorn.run(app, host="0.0.0.0", port=8000)