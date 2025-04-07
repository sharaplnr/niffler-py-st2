from pydantic import BaseModel

class Category(BaseModel):
    id: str = None
    name: str
    username: str = None
    archived: bool = None

class CategoryRequest(BaseModel):
    id: str
    category: Category
    username: str

class CategoriesResponse(BaseModel):
    id: str = None
    name: str
    username: str = None
    archived: bool = None