from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schema

from database import get_db
from typing import List

from routers.users import get_current_admin
router = APIRouter(
    prefix="/stock",
    tags=["stock"],
)

# 获取商品的库存
@router.get("/{product_id}", response_model=schema.Stock)
def get_stock(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.ProductStock).filter(models.ProductStock.ProductID == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="商品未找到")
    return product

# 获取所有商品的库存
@router.get("/", response_model=List[schema.Stock])
def get_all_stock(db: Session = Depends(get_db)):
    products = db.query(models.ProductStock).all()
    return products