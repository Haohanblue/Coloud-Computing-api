# routers/admin.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schema
from database import get_db
import datetime

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

# 获取所有订单
@router.get("/orders", response_model=List[schema.Order])
def get_all_orders(db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
    return orders

# 查询某一个订单
@router.get("/orders/{order_id}", response_model=schema.Order)
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.OrderID == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="订单未找到")
    return order

# 查询所有用户
@router.get("/users", response_model=List[schema.User])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users
# 查询某一个人的订单
@router.get("/users/{user_id}/orders", response_model=List[schema.Order])
def get_user_orders(user_id: str, db: Session = Depends(get_db)):
    orders = db.query(models.Order).filter(models.Order.UserID == user_id).all()
    return orders



# 制作完成订单接口,将订单状态改为已完成
@router.put("/orders/{order_id}/complete", response_model=schema.Order)
def complete_order(order_id: str, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.OrderID == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="订单未找到")
    db_order.OrderStatus = "已完成"
    db_order.OrderCompleteDate = datetime.datetime.now()
    db.commit()
    db.refresh(db_order)
    # 减少库存
    order_items = db.query(models.OrderItem).filter(models.OrderItem.OrderID == order_id).all()
    for item in order_items:
        product = db.query(models.Product).filter(models.Product.ProductID == item.ProductID).first()
        product.Stock -= item.Quantity
        db.commit()
        print(f"成功减少了{product.ProductID}的库存,现在的库存是{product.Stock}")
    return db_order



# 修改库存数量
@router.put("/stock", response_model=schema.Stock)
def update_stock(stock: schema.Stock, db: Session = Depends(get_db)):
    product_id = stock.ProductID
    db_product = db.query(models.ProductStock).filter(models.ProductStock.ProductID == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="产品未找到")
    db_product.Stock = stock.Stock
    db.commit()
    db.refresh(db_product)
    return db_product

# 管理员添加商品
@router.post("/product", response_model=schema.Product)
def create_product(product: schema.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    # 添加库存
    db_stock = models.ProductStock(ProductID=db_product.ProductID, Stock=0)
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_product

# 管理员更新商品
@router.put("/product/{product_id}", response_model=schema.Product)
def update_product(product_id: int, product: schema.ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.ProductID == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="商品未找到")
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

# 管理员删除商品
@router.post("/product/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.ProductID == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="商品未找到")
    #先去删除库存
    db_stock = db.query(models.ProductStock).filter(models.ProductStock.ProductID == product_id).first()
    db.delete(db_stock)
    #再删除商品
    db.delete(db_product)
    db.commit()
    db.refresh(db_product)

    return {"message": "商品已删除"}

