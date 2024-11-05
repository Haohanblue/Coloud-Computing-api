# Cloud Computing
<<<<<<< HEAD
## 使用poetry包管理工具
## python版本3.11.9
### 安装poetry
```pip install poetry``` 
### 安装poetry虚拟环境
```poetry shell``` 
### 安装项目依赖
```poetry install``` 
### 启动项目
```poetry run python app/main.py``` 

### 需要添加的环境变量
app/database.py下的`DATABASE_URL`

app/llm/llm.py下的`ZHIPUAI_API_KEY`

app/createData.py下的`connection`

app/routers/users.py下的simulate_send_sms函数里的`values中的互亿账号和密码`

app/routers/orders.py下的七相支付的商户号和密钥，即`pid`和`key`
=======
 
>>>>>>> 8e42b19 (Initial commit)
