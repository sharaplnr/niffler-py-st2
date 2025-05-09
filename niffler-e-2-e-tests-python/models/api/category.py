from pydantic import BaseModel

class Category(BaseModel):
    id: str | None = None
    name: str
    username: str | None = None
    archived: bool | None = None

class CategoryRequest(Category):
    pass

class CategoriesResponse(Category):
    pass