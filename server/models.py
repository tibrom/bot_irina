import datetime
from typing import Optional, List, Dict
from typing import Any
from pydantic import BaseModel, EmailStr, validator, constr




class MessageType(BaseModel):
    tg_id: str
    id: str
    detali: str
    recipient: Optional[str] = None



