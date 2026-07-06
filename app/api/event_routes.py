from fastapi import APIRouter

from app.services.event_service import get_events

router = APIRouter(prefix='/events', tags=['Events'])


@router.get('')
def events(limit: int = 50):
    return get_events(limit)
