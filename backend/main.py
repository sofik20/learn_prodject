from fastapi import FastAPI, HTTPException, status
from database import init_db
from schemas import ProductCreate, ProductUpdate, ProductPatch
import crud

app = FastAPI(title="Фермерский дворик API")


@app.on_event("startup")
def startup():
    """Создаёт таблицу при запуске сервера"""
    init_db()


# ========== GET ==========

@app.get("/products")
def read_products():
    """Получить список всех продуктов"""
    return crud.get_all_products()


@app.get("/products/{product_id}")
def read_product(product_id: int):
    """Получить продукт по ID"""
    product = crud.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    return product


# ========== POST ==========

@app.post("/products", status_code=status.HTTP_201_CREATED)
def add_product(product: ProductCreate):
    """Создать новый продукт"""
    new_id = crud.create_product(product.model_dump())
    return {"message": "Продукт создан", "id": new_id}


# ========== PUT ==========

@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductUpdate):
    """Полностью обновить продукт"""
    existing = crud.get_product_by_id(product_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    crud.update_product(product_id, product.model_dump())
    return {"message": "Продукт обновлён"}


# ========== PATCH ==========

@app.patch("/products/{product_id}")
def patch_product(product_id: int, product: ProductPatch):
    """Частично обновить продукт"""
    existing = crud.get_product_by_id(product_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Продукт не найден")

    # Берём только те поля, которые переданы
    updated_data = product.model_dump(exclude_unset=True)

    # Объединяем существующие данные с новыми
    for key, value in updated_data.items():
        existing[key] = value

    crud.update_product(product_id, existing)
    return {"message": "Продукт частично обновлён"}


# ========== DELETE ==========

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    """Удалить продукт"""
    existing = crud.get_product_by_id(product_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    crud.delete_product(product_id)
    return {"message": "Продукт удалён"}