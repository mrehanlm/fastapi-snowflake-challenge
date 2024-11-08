from typing import Optional

from pydantic import BaseModel, EmailStr


class ClientSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str]
    email: Optional[EmailStr]
