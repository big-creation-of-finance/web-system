from threading import Lock

# 简易demo数据库类，负责程序所有数据操作（读写或其他待开发功能）
class Data:
    data=1
    lock=Lock()

    def __init__(self):
        pass
    
    def read(self)->int:
        return self.data

    def write(self,data:int)->None:
        self.lock.acquire()
        self.data=data
        self.lock.release()