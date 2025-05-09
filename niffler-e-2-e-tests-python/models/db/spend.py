from datetime import datetime
from sqlmodel import SQLModel, Field
from models.db.category import Category


class Spend(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    amount: float
    description: str
    category: Category
    spendDate: datetime
    currency: str