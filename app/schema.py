from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# 用户模型
class UserBase(BaseModel):
    PhoneNumber: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    UserID: str
    RegisteredDate: datetime
    IsAdmin: bool

    class Config:
        from_attributes = True

class VerifyCodeInput(BaseModel):
    PhoneNumber: str
    Code: str

# 商品模型
class ProductBase(BaseModel):
    CategoryID: int
    CategoryName: str
    ProductName: str
    Price: Decimal
    Description: Optional[str] = None
    ImageURL: Optional[str] = None

class ProductCreate(ProductBase):
    CategoryID: int
    CategoryName: str
    pass

class ProductUpdate(BaseModel):
    CategoryID: Optional[int] = None
    CategoryName: Optional[str] = None
    ProductName: Optional[str] = None
    Price: Optional[Decimal] = None
    Description: Optional[str] = None
    ImageURL: Optional[str] = None

class Product(ProductBase):
    ProductID: int
    CreatedDate: datetime

    class Config:
        from_attributes = True

# 购物车项模型
class CartItemBase(BaseModel):
    ProductID: int
    Quantity: int
    Size: Optional[str] = "中杯"
    Ice: Optional[str] = "正常冰"
    Sugar: Optional[str] = "正常糖"

class CartItemCreate(CartItemBase):
    pass

class CartItem(CartItemBase):
    CartItemID: str
    AddedDate: datetime
    product: Product

    class Config:
        from_attributes = True

# 订单项模型
class OrderItemBase(BaseModel):
    ProductID: int
    Quantity: int
    UnitPrice: Decimal
    TotalPrice: Decimal

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    OrderItemID: int
    product: Product
    Ice: Optional[str] = "正常冰"
    Size: Optional[str] = "中杯"
    Sugar: Optional[str] = "正常糖"

    class Config:
        from_attributes = True

# 订单模型
class OrderBase(BaseModel):
    TotalAmount: Decimal
    OrderStatus: Optional[str] = "待支付"
    UserID: str

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    OrderStatus: Optional[str] = None

    class Config:
        from_attributes = True

class Order(OrderBase):
    OrderID: str
    OrderCreateDate: datetime
    order_items: List[OrderItem]
    OrderPayDate: Optional[datetime]
    OrderCompleteDate: Optional[datetime]
    OrderNumber: Optional[str]


    class Config:
        from_attributes = True

class QuantityChange(BaseModel):
    amount: int 

class Stock(BaseModel):
    ProductID: int
    Stock: int
    pass