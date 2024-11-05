import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schema
import hashlib
from database import get_db
from typing import List
from routers.users import get_current_user
import datetime
import nanoid
from sqlalchemy import func
router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

# 提交订单
@router.post("/", response_model=schema.Order)
def create_order(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    cart_items = db.query(models.CartItem).filter(models.CartItem.UserID == current_user.UserID).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="购物车为空")
    total_amount = sum(item.Quantity * item.product.Price for item in cart_items)
    print(datetime.datetime.now())
    db_order = models.Order(UserID=current_user.UserID, TotalAmount=total_amount,OrderID = nanoid.generate(size=16),OrderCreateDate = datetime.datetime.now())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
   
    for item in cart_items:
        db_order_item = models.OrderItem(
            OrderID=db_order.OrderID,
            ProductID=item.ProductID,
            Quantity=item.Quantity,
            UnitPrice=item.product.Price,
            TotalPrice=item.Quantity * item.product.Price,
            Size=item.Size,
            Ice=item.Ice,
            Sugar=item.Sugar,
        )

        db.add(db_order_item)
    db.query(models.CartItem).filter(models.CartItem.UserID == current_user.UserID).delete()
    db.commit()
    return db_order

# 获取用户的订单列表
@router.get("/", response_model=List[schema.Order])
def get_user_orders(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    orders = db.query(models.Order).filter(models.Order.UserID == current_user.UserID).all()
    return orders

# 获取订单详情
@router.get("/{order_id}", response_model=schema.Order)
def get_order_detail(order_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    order = db.query(models.Order).filter(models.Order.OrderID == order_id, models.Order.UserID == current_user.UserID).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单未找到")
    return order

@router.post("/{order_id}/pay/alipay")
def pay_order(order_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    order = db.query(models.Order).filter(models.Order.OrderID == order_id, models.Order.UserID == current_user.UserID).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单未找到")
    else:
        # 总金额转化为字符串
        total_amount = str(order.TotalAmount)
        para_list = {
            "type" : "alipay",
            "out_trade_no"	: order_id,
            "name"	: "饮料",
            "money"	: total_amount,
            "clientip"	: "192.168.1.100",
            "device" : "jump"
        }
        result = DO_AlyPay(para_list)
        print(result)
        return result
    
@router.post("/{order_id}/pay/wxpay")
def pay_order(order_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    order = db.query(models.Order).filter(models.Order.OrderID == order_id, models.Order.UserID == current_user.UserID).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单未找到")
    else:
        # 总金额转化为字符串
        total_amount = str(order.TotalAmount)
        para_list = {
            "type" : "wxpay",
            "out_trade_no"	: str(order_id),
            "name"	: "饮料",
            "money"	: total_amount,
            "clientip"	: "192.168.1.100",
            "device" : "jump"
        }
        result = DO_AlyPay(para_list)
        print(result)
        return result
    
# 查询订单支付状态
@router.get("/getPayResult/{order_id}")
def get_pay_result(order_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    print("查询支付结果")
    order = db.query(models.Order).filter(models.Order.OrderID == order_id, models.Order.UserID == current_user.UserID).first()
    print(order)
    if not order:
        raise HTTPException(status_code=404, detail="订单未找到")
    else:
        result = GetPayResult(order_id)
        if result["status"] == "1":
            print("支付成功")
            # 更新订单状态
            now = datetime.datetime.now()
            order.OrderStatus = "待取餐"
            order.OrderPayDate = now
            # 根据今日日期内的订单，OrderNumber按照取号码的倒序排列，取第一个取号码，然后加1，作为该订单的取号码
            today = datetime.date.today()
            print(now.date() == today)
            # 寻找第一个取号码，但是要排除自己呀
            order_number = db.query(models.Order).filter(func.date(models.Order.OrderPayDate) == today,models.Order.OrderID != order_id).order_by(models.Order.OrderNumber.desc()).first()
            if order_number:
                order.OrderNumber = int(order_number.OrderNumber) + 1
            else:
                order.OrderNumber = 1
            db.commit()
            db.refresh(order)
        else:
            print("支付失败")
            # 调用支付失败的函数
        print(result)
        # 将支付url返回
        return result






# 异步回调通知
@router.get("/notify")
def notify(req):
    print(req)
    return {"message": "success"}


def GetPayResult(order_id):
    print("开始发送接口了")
    pid = "" # 商户号
    key = "" # 商户密钥
    url = f"https://api.payqixiang.cn/api.php?act=order&pid={pid}&key={key}&out_trade_no={order_id}"
    response_result = requests.get(url).json()
    return response_result


def DO_AlyPay(para_list):

    partner= "" # 商户号
    key= "" # 商户密钥
    notify_url= "http://haohan.space:2301/orders/notify"
    return_url= f"http://haohan.space:2300/payresult"
    sitename = 'haohan.space'
    
    para_list['pid'] = partner
    para_list['notify_url'] = notify_url
    para_list['return_url'] = return_url
    para_list['sitename'] = sitename
    para_list['sign'] = ""
    para_list['sign_type'] = "MD5"
    print(para_list) 
    # 生成签名
    para_list_filter = {} # sign、sign_type、和空值不参与签名
    for k,v in para_list.items():
        if k == "sign"  or k == "sign_type" or v == "":
            continue
        else:
            para_list_filter[k] = v
    
    # 按照ASCII码从小到大排序（a-z）
    para_list_sorted = sorted(para_list_filter)
    print(para_list_sorted)
    print(type(para_list_sorted))
    para_str = "" # 组成a=b&c=d&e=f，参数值不要进行url编码
    for k in para_list_sorted:
       para_str += "&" + k + "=" + para_list_filter[k]

    sign_str = para_str[1:] + key # 拼接好的字符串与商户密钥KEY进行MD5加密得出sign签名参数
    sign = hashlib.md5(sign_str.encode(encoding='utf-8')).hexdigest()

    para_list['sign'] = sign # 将sign写入post 提交参数
    print(sign)
    print(para_list)
    # 提交api
    url =  "https://api.payqixiang.cn/mapi.php"
    headers = {"Content-Type":"application/x-www-form-urlencoded",
               "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"}
    response_result = requests.post(url, data=(para_list), headers=headers)
    response_text = eval(response_result.text)
    print(response_text)
    # print(response_text)
    code = response_text['code']
    trade_no = response_text['trade_no']
    payurl = response_text['payurl']
    #去掉返回的支付链接中的转义字符
    payurl = payurl.replace("\\", "")

    if code != 1:
        return {"ret": response_text['code']}

    return {
        "code":code,
        "trade_no":trade_no,
        "payurl":payurl
        }