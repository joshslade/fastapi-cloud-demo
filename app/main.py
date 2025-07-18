from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
from http import HTTPStatus

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import Response
from sheets import duplicate_data_in_sheet

app = FastAPI(title="FastAPI Demo")

@app.get("/ping", tags=["health"])
async def ping():
    return JSONResponse({"status": "ok"})


@app.get("/hello/{name}")
async def hello(name: str):
    return {"message": f"Hello, {name}!"}




class GSheetSchema(BaseModel):
    """Schema of GSheet Request"""
    sheet_id: str


@app.post("/dup")
async def dup_sheets(data: GSheetSchema) -> Response:
    print(data)
    response = duplicate_data_in_sheet(data.sheet_id)

    return Response(
        content=json.dumps({"message": "Request received!", "response":response}),
        status_code=HTTPStatus.ACCEPTED,
    )
