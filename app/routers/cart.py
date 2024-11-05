from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schema
from database import get_db
from typing import List
from routers.users import get_current_user
import nanoid
router = APIRouter(
    prefix="/cart",
    tags=["cart"],
)

# 获取购物车内容
@router.get("/", response_model=List[schema.CartItem])
def get_cart_items(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    print(f"正在获取{current_user.UserID}的购物车")
    cart_items = db.query(models.CartItem).filter(models.CartItem.UserID == current_user.UserID).all()
    return cart_items

# 添加商品到购物车
@router.post("/", response_model=schema.CartItem)
def add_to_cart(cart_item: schema.CartItemCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    product = db.query(models.Product).filter(models.Product.ProductID == cart_item.ProductID).first()
    if product is None: 
        raise HTTPException(status_code=404, detail="商品未找到")
    # 检查购物车中是否已经有该商品
    cart_item_in_db = db.query(models.CartItem).filter(models.CartItem.ProductID == cart_item.ProductID, models.CartItem.Size == cart_item.Size, models.CartItem.Ice == cart_item.Ice, models.CartItem.Sugar == cart_item.Sugar,models.CartItem.UserID == current_user.UserID).first()
    if cart_item_in_db is not None:
        cart_item_in_db.Quantity += cart_item.Quantity
        # 更新购物车项
        db.commit()
        db.refresh(cart_item_in_db)
        # 如果数量小于等于0，则删除购物车项
        if cart_item_in_db.Quantity <= 0:
            #调用删除购物车项的接口
            db.delete(cart_item_in_db)
            db.commit()
            return cart_item_in_db
        return cart_item_in_db
    else:
        print("执行到我了")
        if cart_item.Quantity <= 0:
            print("数量小于等于0")
            # 数量小于等于0，不添加购物车项
            raise HTTPException(status_code=400, detail="数量必须大于0")
        
        else:
            print("数量大于0")
            cart_item = models.CartItem(**cart_item.dict(), UserID=current_user.UserID, CartItemID=nanoid.generate(size=16))
            db.add(cart_item)
            db.commit()
            db.refresh(cart_item)
            print(cart_item)
            return cart_item
# 根据CartItemId增加或减少购物车中的商品数量,根据请求体为add或reduce判断+1或-1
@router.put("/{cart_item_id}")
def add_or_reduce_cart_item(cart_item_id: str, action: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    cart_item = db.query(models.CartItem).filter(models.CartItem.CartItemID == cart_item_id, models.CartItem.UserID == current_user.UserID).first()
    if cart_item is None:
        raise HTTPException(status_code=404, detail="购物车项未找到")
    if action == "add":
        cart_item.Quantity += 1
    elif action == "reduce":
        cart_item.Quantity -= 1
    else:
        raise HTTPException(status_code=400, detail="请求体错误")
    db.commit()
    db.refresh(cart_item)
    if cart_item.Quantity <= 0:
        db.delete(cart_item)
        db.commit()
    return cart_item


# 删除购物车中的某个商品
@router.delete("/{cart_item_id}")
def delete_cart_item(cart_item_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    cart_item = db.query(models.CartItem).filter(models.CartItem.CartItemID == cart_item_id, models.CartItem.UserID == current_user.UserID).first()
    if cart_item is None:
        raise HTTPException(status_code=404, detail="购物车项未找到")
    db.delete(cart_item)
    db.commit()
    return {"message": "已删除购物车项"}


# 清空购物车
@router.delete("/")
def delete_cart_item(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    cart_items = db.query(models.CartItem).filter(models.CartItem.UserID == current_user.UserID).all()
    for cart_item in cart_items:
        db.delete(cart_item)
    db.commit()
    return {"message": "已清空购物车"}


