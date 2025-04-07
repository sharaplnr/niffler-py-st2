from datetime import datetime

from pydantic import BaseModel
from models.api.category import Category

class SpendRequest(BaseModel):
    id: str = None
    amount: float
    description: str
    category: Category
    spendDate: str
    currency: str

class SpendResponse(BaseModel):
    id: str = None
    amount: float
    description: str
    category: Category
    spendDate: str
    currency: str