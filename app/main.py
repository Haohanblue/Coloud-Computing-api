from fastapi import FastAPI
from routers import users, products, cart, orders, admin, stock
from llm import zhipu
from database import engine
import models as models
import sys

sys.path.append('..')
# 解决跨域问题
from fastapi.middleware.cors import CORSMiddleware
# 允许所有域名访问
origins = [
    "http://localhost:5173",
]



models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(users.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(admin.router)
app.include_router(stock.router)
app.include_router(zhipu.router)

@app.get("/")
def read_root():
    return {"message": "咖啡店点餐系统API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)