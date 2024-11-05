from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, DECIMAL, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
nowTime = datetime.now()
class User(Base):
    __tablename__ = 'users'
    UserID = Column(String(20), primary_key=True, index=True)
    PhoneNumber = Column(String(20), unique=True, nullable=False)
    IsAdmin = Column(Boolean, default=False)
    RegisteredDate = Column(DateTime, default=nowTime)

    cart_items = relationship("CartItem", back_populates="user")
    orders = relationship("Order", back_populates="user")

class Product(Base):
    __tablename__ = 'products'
    CategoryID = Column(Integer, nullable=False)
    CategoryName = Column(String(50), nullable=False)
    ProductID = Column(Integer, primary_key=True, index=True)
    ProductName = Column(String(100), nullable=False)
    Price = Column(DECIMAL(10, 2), nullable=False)
    Description = Column(String(500))
    ImageURL = Column(String(200))
    CreatedDate = Column(DateTime, default=nowTime)

class CartItem(Base):
    __tablename__ = 'cart_items'
    CartItemID = Column(String(20), primary_key=True, index=True)
    UserID = Column(String(20), ForeignKey('users.UserID'))
    ProductID = Column(Integer, ForeignKey('products.ProductID'))
    Quantity = Column(Integer, nullable=False)
    AddedDate = Column(DateTime, default=nowTime)
    Size = Column(String(50), nullable=False, default="中杯")
    Ice = Column(String(50), nullable=False, default="正常冰")
    Sugar = Column(String(50), nullable=False, default="正常糖")

    user = relationship("User", back_populates="cart_items")
    product = relationship("Product")

class Order(Base):
    __tablename__ = 'orders'
    OrderID = Column(String(20), primary_key=True)
    UserID = Column(String(20), ForeignKey('users.UserID'))
    OrderCreateDate = Column(DateTime, default=nowTime)
    TotalAmount = Column(DECIMAL(10, 2), nullable=False)
    OrderStatus = Column(String(50), default="待支付")
    OrderPayDate = Column(DateTime)
    OrderCompleteDate = Column(DateTime)
    OrderNumber = Column(String(50))

    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = 'order_items'
    OrderItemID = Column(Integer, primary_key=True)
    OrderID = Column(String(20), ForeignKey('orders.OrderID'))
    ProductID = Column(Integer, ForeignKey('products.ProductID'))
    Quantity = Column(Integer, nullable=False)
    UnitPrice = Column(DECIMAL(10, 2), nullable=False)
    TotalPrice = Column(DECIMAL(10, 2), nullable=False)
    Size = Column(String(50), nullable=False, default="中杯")
    Ice = Column(String(50), nullable=False, default="正常冰")
    Sugar = Column(String(50), nullable=False, default="正常糖")

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product")

class ProductStock(Base):
    __tablename__ = 'product_stock'
    ProductID = Column(Integer, ForeignKey('products.ProductID'), primary_key=True)
    Stock = Column(Integer, nullable=False)
    product = relationship("Product")