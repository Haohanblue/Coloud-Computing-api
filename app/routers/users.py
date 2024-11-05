from fastapi import APIRouter, Depends, HTTPException, Response, BackgroundTasks, Request
from sqlalchemy.orm import Session
import models
import schema
from database import get_db
from datetime import datetime, timedelta
import random
import urllib.parse
import urllib.request
import hmac
import hashlib
import nanoid
router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# 定义服务器密钥
SECRET_KEY = "haohanblue"  # 请替换为你的实际密钥

# 模拟验证码存储
verification_codes = {}

def generate_token(user_id):
    message = str(user_id).encode()
    signature = hmac.new(SECRET_KEY.encode(), message, hashlib.sha256).hexdigest()
    token = f"{user_id}:{signature}"
    return token

def verify_token(token):
    try:
        user_id_str, signature = token.split(':')
        expected_signature = hmac.new(SECRET_KEY.encode(), user_id_str.encode(), hashlib.sha256).hexdigest()
        if hmac.compare_digest(expected_signature, signature):
            return user_id_str
        else:
            return None
    except Exception:
        return None

def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("user_token")
    print(token)
    if token is None:
        raise HTTPException(status_code=401, detail="未认证")
    user_id = verify_token(token)
    print(user_id)
    if user_id is None:
        raise HTTPException(status_code=401, detail="认证过期或无效")
    db_user = db.query(models.User).filter(models.User.UserID == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=401, detail="用户无效")
    return db_user

def get_current_admin(current_user: models.User = Depends(get_current_user)):
    if not current_user.IsAdmin:
        raise HTTPException(status_code=403, detail="无权限")
    return current_user

# 请求登录验证码
@router.post("/request-login-code")
def request_login_code(user_phone: schema.UserBase, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    phone_number = user_phone.PhoneNumber
    # 检查用户是否存在，如果不存在则创建
    db_user = db.query(models.User).filter(models.User.PhoneNumber == phone_number).first()
    if not db_user:
        db_user = models.User(PhoneNumber=phone_number, UserID=nanoid.generate(size=16))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    # 生成4位验证码
    verification_code = str(random.randint(1000, 9999))
    # 存储验证码，设置过期时间
    verification_codes[phone_number] = {
        "code": verification_code,
        "expires": datetime.utcnow() + timedelta(minutes=5)
    }
    # 模拟发送短信
    background_tasks.add_task(simulate_send_sms, phone_number, verification_code)
    return {"message": "验证码已发送"}

def simulate_send_sms(phone_number, code):
    url = 'http://106.ihuyi.com/webservice/sms.php?method=Submit'
    values = {
        'account':'', # 用户名
        'password':'', # 密码
        'mobile':phone_number,
        'content':f'您的验证码是：{code}。请不要把验证码泄露给其他人。',
        'format':'json',
    }
    data = urllib.parse.urlencode(values).encode(encoding='UTF8')
    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    res = response.read()
    print(res.decode("utf8"))
    print(f"发送短信到 {phone_number}，验证码是 {code}")

# 验证验证码并登录
@router.post("/verify-code")
def verify_code(user_input: schema.VerifyCodeInput, response: Response, db: Session = Depends(get_db)):
    phone_number = user_input.PhoneNumber
    code = user_input.Code
    if phone_number not in verification_codes:
        raise HTTPException(status_code=400, detail="未请求验证码")
    stored_code_info = verification_codes[phone_number]
    if datetime.utcnow() > stored_code_info["expires"]:
        del verification_codes[phone_number]
        raise HTTPException(status_code=400, detail="验证码已过期")
    if stored_code_info["code"] != code:
        raise HTTPException(status_code=400, detail="验证码错误")
    # 验证成功，删除验证码
    del verification_codes[phone_number]
    # 获取用户
    db_user = db.query(models.User).filter(models.User.PhoneNumber == phone_number).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="用户未找到")
    # 生成加密的token
    token = generate_token(db_user.UserID)
    # 设置cookie，设置httponly和secure属性，防止XSS和CSRF攻击
    response.set_cookie(key="user_token", value=token)
    return {"message": "登录成功","cookie": {"user_token": token}}
# 获取当前用户信息
@router.get("/me")
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user
# 注销
@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="user_token")
    return {"message": "已注销"}
