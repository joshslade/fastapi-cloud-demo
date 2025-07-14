from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="FastAPI Demo")

@app.get("/ping", tags=["health"])
async def ping():
    return JSONResponse({"status": "ok"})

@app.get("/hello/{name}")
async def hello(name: str):
    return {"message": f"Hello, {name}!"}