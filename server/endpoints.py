from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request

from .depends import get_main_reposytory
from .models import MessageType
from .repositories import MainRepository
from core.logger import logger





router = APIRouter()


@router.post('/send-message')
async def send_new_message(
    new: MessageType,
    message_type: MainRepository =Depends(get_main_reposytory)
):
    return await message_type.send_message(message=new)


@router.post('/echo')
async def echo_request(request: Request):
    request_body = "None"
    request_headers = "None"
    request_data = "None"
    try:
        request_body = await request.body()
    except:
        pass
    try:
        request_headers = dict(request.headers)
    except:
        pass
    try:
        request_data = await request.json()
    except:
        pass
    logger.debug(f"request_body {request_body}")
    logger.debug(f"request_headers {request_headers}")
    logger.debug(f"request_data {request_data}")