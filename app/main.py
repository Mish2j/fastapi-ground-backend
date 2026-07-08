"""
Description:
Python FastAPI ground-software simulator with modular telemetry generation, command validation, event logging, WebSocket broadcasting, and REST APIs for dashboard (later Open MCT) integration.


1. Backend creates telemetry
2. Backend sends telemetry through WebSocket
3. Frontend displays telemetry
4. User sends command through REST
5. Backend validates command
6. Backend changes simulator state
7. New telemetry reflects that change
8. Event log records what happened

Real-time flow:
simulator.py
  ↓ generates telemetry
telemetry_service.py
  ↓ saves latest/history
connection_manager.py
  ↓ broadcasts to clients
websocket_routes.py
  ↓ sends to frontend/Open MCT

Command flow:
POST /commands
  ↓
command_routes.py
  ↓
command_service.py
  ↓
command_handler.py
  ↓
satellite_state.py updates
  ↓
event_log.py records event
  ↓
next telemetry shows new state
"""

# FastAPI is a Python class that provides all the functionality for your API.
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.api.telemetry_routes import router as telemetry_router
from app.api.command_routes import router as command_router
from app.api.event_routes import router as event_router
from app.api.room_routes import router as room_router
from app.realtime.websocket_routes import router as websocket_router

app = FastAPI(
    title='Mission Telemetry Backend'
)  # app variable will be an "instance" of the class FastAPI

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:5173',
        'http://127.0.0.1:5173',
        'http://localhost:3000',
        'http://127.0.0.1:3000',
        'null',
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(telemetry_router)
app.include_router(command_router)
app.include_router(event_router)
app.include_router(websocket_router)
app.include_router(room_router)


# ------------ GET ------------
# path operation function
@app.get(
    '/'
)  # tells FastAPI that the function right below is in charge of handling requests that go to the path /
async def root():
    return {'message': 'Mission Telemetry Backend'}


@app.get('/health')
def health_check():
    return {'status': 'ok'}
