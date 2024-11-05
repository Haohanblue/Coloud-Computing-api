from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "这里输入你的数据库连接地址"

engine = create_engine(
    DATABASE_URL,
    echo=True,  # 输出SQL语句，方便调试
    pool_pre_ping=True  # 检查连接是否有效
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()