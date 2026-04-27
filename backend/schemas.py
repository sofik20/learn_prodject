from pydantic import BaseModel, Field
from typing import Optional


class ProductCreate(BaseModel):
    """Схема для создания нового продукта"""
    name: str = Field(..., min_length=2, max_length=100, description="Название продукта")
    category: str = Field(..., min_length=2, max_length=50, description="Категория (овощи, молочка, мясо и т.д.)")
    price: float = Field(..., gt=0, description="Цена за единицу (руб.)")
    quantity: int = Field(..., ge=0, description="Количество в наличии")
    farm: str = Field(..., min_length=2, max_length=100, description="Название фермы")
    organic: bool = Field(..., description="Органический продукт (да/нет)")


class ProductUpdate(BaseModel):
    """Схема для полного обновления продукта (PUT)"""
    name: str
    category: str
    price: float
    quantity: int
    farm: str
    organic: bool


class ProductPatch(BaseModel):
    """Схема для частичного обновления продукта (PATCH)"""
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    farm: Optional[str] = None
    organic: Optional[bool] = None


class ProductRead(BaseModel):
    """Схема для чтения продукта из базы"""
    id: int
    name: str
    category: str
    price: float
    quantity: int
    farm: str
    organic: bool