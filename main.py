from typing import Annotated
from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import json
# JSONResponse
# PlainTextResponse
# HTMLResponse
# FileResponse
# RedirectResponse

app=FastAPI() #產生FastAPI物件
# 利用 uvicorn去啟動伺服器在 http://127.0.0.1:8000
# 更改埠號  uvicorn main:app --reload --port 3000(--port 輸入要更改的埠號)
# 利用路由的設定，處理路徑("/")
# @app.get("/")
# def index():
#     return FileResponse("home.html")

# @app.get("/img/logo")
# def logo():
#     return FileResponse("cat.png")

# 非靜態檔案處理的路由，擺在上方

# 處理 GET 方法的路徑 /test
@app.get("/test")
def test():
    return {"data":10,"method":"GET"}

# 處理 POST 方法的路徑 /test
@app.post("/add")
def testPost(body=Body(None)):
    # 如果是中文需解碼
    # body=body.decode("utf-8")
    data=json.loads(body)
    result=data["n1"]+data["n2"]
    return {"ok":True,"method":"POST","result":result}

@app.get("/member")
def member():
    return RedirectResponse("/")

# 利用路由的設定，處理路徑/data
@app.get("/data")
def getData():
    return {"data":[2,3,1]}

# 使用路徑參數，處理擁有相同前綴字的路徑
# 想讓前端可以透過網址，輸入一個數字，後端把輸入的數字做平方，再回應給前端
@app.get("/square")
def square(number: Annotated[int,Query(ge=1)]): #路徑參數必須為數字的資料型態，否則後端會拒絕程式進入主要邏輯中
    #路徑參數預設為字串型態，所以要先轉換為整數
    number=int(number)
    return {"result":number*number}

#處理路徑 /echo/名字
@app.get("/echo/{name}")
def echo(name:Annotated[str,Path(min_length=2,max_length=30)]):
    return{"message":"Hello"+name}

# 要求字串的設定
# 處理路徑 /hello?name=名字
@app.get("/hello")
def hello(name:Annotated[str,Query(min_length=2)]):
    message="哈囉，"+name
    return {"message":message}

# 處理路徑 /multiply?n1=數字&n2=數字
@app.get("/multiply")
def multiply(
    n1:Annotated[int,Query(ge=0)],
    n2:Annotated[int,Query(ge=0)]
):
    n1=int(n1)
    n2=int(n2)
    result=n1*n2
    return {"result":result}

# 路徑參數的驗證
# 驗證、拒絕非整數int的資料 def square(number:Annotated[int,None]):
# 驗證、拒絕非整數或浮點數float的資料 def square(number:Annotated[float,None]):
# 驗證、拒絕不在特定範圍中的整數
# Path 代表針對路徑參數做驗證 gt代表大於; lt代表小於; ge代表大於等於; le代表小於等於
# @app.get("/square/{number}")
# def square(
#     number:Annotated[int, Path(gt=3,lt=10)]
# ):
#     number=int(number)
#     return {"result":number*number}
# 驗證、拒絕不在特定長度中的字串str，min_length代表最小字元數，max_length代表最大字元數


# 要求字串的驗證
# Query 代表針對要求字串做驗證
# @app.get("/multiply")
# def multiply(
#     n1:Annotated[int, Query(ge=-10,le=10)], 
#     n2:Annotated[int, Query(ge=-10,le=10)]
# ):
#     n1=int(n1)
#     n2=int(n2)
#     result=n1*n2
#     return {"result":result}
# 驗證、拒絕不在特定長度中的字串str，min_length代表最小字元數，max_length代表最大字元數

#統一處理靜態檔案，擺在下方才不會影響其他路由
# app.mount("網址路徑前綴", StaticFiles(directory="子資料夾名稱"))
app.mount("/", StaticFiles(directory="public", html=True)) #html預設為True，會自動找到index.html

