from fastapi import APIRouter
from app.services.telemetry_service import get_latest, get_history

router = APIRouter(prefix='/telemetry', tags=['Telemetry'])


@router.get('/latest')
def latest_telemetry():
    return get_latest()


@router.get('/history')
def telemetry_history(limit: int = 100):
    return get_history(limit)
