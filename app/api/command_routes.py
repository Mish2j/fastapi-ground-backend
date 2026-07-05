from fastapi import APIRouter

from app.models.command import CommandRequest
from app.services.command_service import execute_command


router = APIRouter(prefix="/commands", tags=["Commands"])

@router.post("")
def send_command(request: CommandRequest):
    return execute_command(request)