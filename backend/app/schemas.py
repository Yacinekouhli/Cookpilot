from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RecipeRequest(BaseModel):
    ingredients: str
    style: Optional[str] = None


class RecipeResponse(BaseModel):
    generated_name: str
    ingredients: str
    steps: str


class RecipeOut(BaseModel):  # utilisé dans GET
    id: int
    ingredients: str
    generated_name: str
    steps: str
    style: Optional[str]
    timestamp: datetime

    class Config:
        orm_mode = True
