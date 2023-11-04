from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from .depends import get_main_reposytory
from .models import MessageType
from .repositories import MainRepository





router = APIRouter()


@router.post('/send-message')
async def send_new_message(
    new: MessageType,
    message_type: MainRepository =Depends(get_main_reposytory)
):
    return await message_type.send_message(message=new)
