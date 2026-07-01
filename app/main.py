from fastapi import FastAPI, WebSocket # FastAPI is a Python class that provides all the functionality for your API.
from fastapi.responses import HTMLResponse
from datetime import datetime
import random
import asyncio

from telemetry import generate_telemetry


app = FastAPI() # app variable will be an "instance" of the class FastAPI


# path operation function
@app.get("/") # tells FastAPI that the function right below is in charge of handling requests that go to the path /
async def root():
    return {"message": "Hello World"}

@app.get("/health")
def health_check():
    return {"status": 'ok'}

@app.get("/telemetry")
def get_telemetry():
    return generate_telemetry()

# TODO: What is websocket used for?
@app.websocket("/ws/telemetry")
async def tel_websocket(websocket: WebSocket):
    await websocket.accept()

    while True:
        data = generate_telemetry()
        await websocket.send_json(data)
        await asyncio.sleep(1)
