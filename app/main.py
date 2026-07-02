# FastAPI is a Python class that provides all the functionality for your API.
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, WebSocketException 
# from fastapi.responses import HTMLResponse
import asyncio
from pydantic import BaseModel

from telemetry import generate_telemetry, get_telemetry_history as telemetry_history, get_latest_telemetry, set_mode


class CommandRequest(BaseModel):
    command: str
    params: dict = {}

app = FastAPI() # app variable will be an "instance" of the class FastAPI

# ------------ GET ------------
# path operation function
@app.get("/") # tells FastAPI that the function right below is in charge of handling requests that go to the path /
async def root():
    return {"message": "Hello World"}


@app.get("/health")
def health_check():
    return {"status": 'ok'}


@app.get("/telemetry/latest")
def get_telemetry_latest():
    return get_latest_telemetry()


@app.get("/telemetry/history")
def get_telemetry_history():
    return telemetry_history()
    
# ------------ POST ------------
@app.post("/commands")
def send_command(request: CommandRequest):
    if request.command == "SET_MODE":
        mode = request.params.get("mode")
        return set_mode(mode)

    return {
        "status": "REJECTED",
        "message": f"Unknown command: {request.command}"
    }


# ------------ websocket ------------
@app.websocket("/ws/telemetry")
async def tel_websocket(websocket: WebSocket):
    await websocket.accept()

    try: 
        while True:
            data = generate_telemetry()
            await websocket.send_json(data)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("Client disconnected")

"""
GET /health
GET /telemetry/latest
GET /telemetry/history?point=battery_voltage&start=...&end=...
WS  /ws/telemetry
POST /commands
"""