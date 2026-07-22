"""
Description:
Python FastAPI ground-software simulator with modular telemetry generation, command validation, event logging, WebSocket broadcasting, and REST APIs for dashboard (later Open MCT) integration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from contextlib import asynccontextmanager

from app.api.telemetry_routes import router as telemetry_router
from app.api.command_routes import router as command_router
from app.api.event_routes import router as event_router
from app.api.room_routes import router as room_router
from app.realtime.websocket_routes import router as websocket_router
from app.api.participant_routes import router as participant_router

from app.constants import ROOM_CLEANUP_INTERVAL_SECONDS
from app.services.room_service import room_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # runs when server starts
    cleanup_task = asyncio.create_task(cleanup_rooms_loop())

    yield  # server is running here

    # runs when server stops
    cleanup_task.cancel()

    try:
        await cleanup_task
    except asyncio.CancelledError:
        pass


app = FastAPI(title='Mission Telemetry Backend', lifespan=lifespan)

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
app.include_router(participant_router)


@app.get('/')
async def root():
    return {'message': 'Mission Telemetry Backend'}


async def cleanup_rooms_loop() -> None:
    while True:
        print('Loop running')
        removed_rooms = room_manager.cleanup_inactive_rooms()

        if removed_rooms:
            print(f'Removed inactive rooms: {removed_rooms}')

        await asyncio.sleep(ROOM_CLEANUP_INTERVAL_SECONDS)
