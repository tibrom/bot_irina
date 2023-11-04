import datetime
from typing import Optional, List, Dict
from typing import Any
from pydantic import BaseModel, EmailStr, validator, constr




class MessageType(BaseModel):
    tg_id: int
    username: str
    detali: str
    addres: str



