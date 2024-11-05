import pymysql
import datetime
# 数据库连接信息
connection = pymysql.connect(
    host='', # 你的数据库地址
    port='', # 你的数据库端口
    user='', # 你的数据库用户名
    password='', # 你的数据库密码
    database='', # 你的数据库名称
    charset='utf8mb4', # 你的数据库编码
    cursorclass=pymysql.cursors.DictCursor # 以字典的方式返回数据
)
try:
    with connection.cursor() as cursor:
        # 创建 product 表（如果不存在）
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS products (
            CategoryID INT,
            CategoryName VARCHAR(255),
            ProductID INT PRIMARY KEY,
            ProductName VARCHAR(255),
            Price DECIMAL(10,2),
            Description TEXT,
            ImageURL VARCHAR(255),
            CreatedDate DATETIME
        ) CHARACTER SET utf8mb4;
        '''
        cursor.execute(create_table_sql)
                # 创建 product 表（如果不存在）

    # 产品列表
        products = [
        {
            "CategoryID": 1,
            "CategoryName": "经典咖啡系列",
            "ProductID": 1,
            "ProductName": "美式咖啡",
            "Price": 19.9,
            "Description": "精选优质咖啡豆精心萃取，呈现纯粹而醇厚的咖啡香气，给您带来最原始的咖啡体验。",
            "ImageURL": "https://img.haohan.space/img/202410302210404.png",
            "CreatedDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "CategoryID": 1,
            "CategoryName": "经典咖啡系列",
            "ProductID": 2,
            "ProductName": "拿铁",
            "Price": 19.9,
            "Description": "浓郁的意式浓缩与丝滑的牛奶完美融合，带来温暖而柔和的口感，享受每一口的细腻香醇。",
            "ImageURL": "https://img.haohan.space/img/202410302217702.png",
            "CreatedDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "CategoryID": 1,
            "CategoryName": "经典咖啡系列",
            "ProductID": 3,
            "ProductName": "摩卡",
            "Price": 23.9,
            "Description": "浓缩咖啡与巧克力的完美邂逅，搭配丝滑奶泡，甜蜜与醇香在舌尖绽放，带来双重享受。",
            "ImageURL": "https://img.haohan.space/img/202410302218470.png",
            "CreatedDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "CategoryID": 1,
            "CategoryName": "经典咖啡系列",
            "ProductID": 4,
            "ProductName": "卡布奇诺",
            "Price": 23.9,
            "Description": "浓郁的意式浓缩搭配绵密的奶泡，口感丰富，香气浓厚，带给您经典的意式咖啡体验。",
            "ImageURL": "https://img.haohan.space/img/202410302217478.png",
            "CreatedDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "CategoryID": 1,
            "CategoryName": "经典咖啡系列",
            "ProductID": 5,
            "ProductName": "焦糖玛奇朵",
            "Price": 23.9,
            "Description": "在香浓的咖啡中融入甜美的焦糖，顶层奶泡带来丝滑口感，甜而不腻，令人回味无穷。",
            "ImageURL": "https://img.haohan.space/img/202410302218502.png",
            "CreatedDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        # 冰淇淋系列
        {
            "CategoryID": 2,
            "CategoryName": "冰淇淋系列",
            "ProductID": 6,
            "ProductName": "摩卡星冰乐",
            "Price": 26.9,
            "Description": "冰爽的摩卡星冰乐，融合咖啡与巧克力的浓郁香气，清凉解暑，提神醒脑。",
            "ImageURL": "https://img.haohan.space/img/202410302218956.png",
            "CreatedDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "CategoryID": 2,
            "CategoryName": "冰淇淋系列",
            "ProductID": 7,
            "ProductName": "巧克力星冰乐",
            "Price": 26.9,
            "Description": "浓郁的巧克力风味，搭配冰沙的爽滑口感，甜蜜冰凉，令人无法抗拒。",
            "ImageURL": "https://img.haohan.space/img/202410302218567.png",
            "CreatedDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "CategoryID": 2,
            "CategoryName": "冰淇淋系列",
            "ProductID": 8,
            "ProductName": "抹茶星冰乐",
            "Price": 26.9,
            "Description": "精选上等抹茶，带来清新的茶香，冰爽的口感让您一扫夏日炎热，焕发活力。",
            "ImageURL": "https://img.haohan.space/img/202410302219060.png",
            "CreatedDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "CategoryID": 2,
            "CategoryName": "冰淇淋系列",
            "ProductID": 9,
            "ProductName": "可可冰淇朵",
            "Price": 19.9,
            "Description": "浓郁的可可风味冰淇淋，入口即化，甜蜜柔滑，带给您双重味觉享受。",
            "ImageURL": "https://img.haohan.space/img/202410302219672.png",
            "CreatedDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        # 纯茶系列
        {
            "CategoryID": 3,
            "CategoryName": "纯茶系列",
            "ProductID": 10,
            "ProductName": "柠檬茶",
            "Price": 14.9,
            "Description": "清新爽口的柠檬茶，酸甜适中，消暑解渴，带来一整天的清新好心情。",
            "ImageURL": "https://img.haohan.space/img/202410302221934.png",
            "CreatedDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "CategoryID": 3,
            "CategoryName": "纯茶系列",
            "ProductID": 11,
            "ProductName": "乌龙茶",
            "Price": 14.9,
            "Description": "传统乌龙茶，茶香浓郁，回甘悠长，品味东方茶道的独特韵味。",
            "ImageURL": "https://img.haohan.space/img/202410302220819.png",
            "CreatedDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "CategoryID": 3,
            "CategoryName": "纯茶系列",
            "ProductID": 12,
            "ProductName": "绿茶",
            "Price": 12.9,
            "Description": "清香扑鼻的绿茶，口感鲜爽，富含天然抗氧化物，健康又解渴。",
            "ImageURL": "https://img.haohan.space/img/202410302221180.png",
            "CreatedDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "CategoryID": 3,
            "CategoryName": "纯茶系列",
            "ProductID": 13,
            "ProductName": "红茶",
            "Price": 12.9,
            "Description": "醇厚的红茶香气，温润暖胃，适合在任何时刻品尝的经典茶饮。",
            "ImageURL": "https://img.haohan.space/img/202410302220721.png",
            "CreatedDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        # 奶茶系列
        {
            "CategoryID": 4,
            "CategoryName": "奶茶系列",
            "ProductID": 14,
            "ProductName": "茉莉奶绿",
            "Price": 14.9,
            "Description": "清新的茉莉香与醇厚的奶香完美结合，口感细腻，令人心旷神怡。",
            "ImageURL": "https://img.haohan.space/img/202410302223505.png",
            "CreatedDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "CategoryID": 4,
            "CategoryName": "奶茶系列",
            "ProductID": 15,
            "ProductName": "芋泥啵啵",
            "Price": 14.9,
            "Description": "浓郁的芋泥风味，搭配Q弹的黑糖珍珠，带来丰富的口感层次，甜蜜满分。",
            "ImageURL": "https://img.haohan.space/img/202410302223397.png",
            "CreatedDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "CategoryID": 4,
            "CategoryName": "奶茶系列",
            "ProductID": 16,
            "ProductName": "伯牙绝弦",
            "Price": 18.9,
            "Description": "独特的配方，融合多种茶香与奶香，口感醇厚，余味悠长，值得细细品味。",
            "ImageURL": "https://img.haohan.space/img/202410302224332.png",
            "CreatedDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "CategoryID": 4,
            "CategoryName": "奶茶系列",
            "ProductID": 17,
            "ProductName": "桂花酿豆腐",
            "Price": 12.9,
            "Description": "细腻的豆腐布丁，融合桂花的清香甜蜜，口感柔滑，甜而不腻，令人难忘。",
            "ImageURL": "https://img.haohan.space/img/202410302224783.png",
            "CreatedDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        # 果茶系列
        {
            "CategoryID": 5,
            "CategoryName": "果茶系列",
            "ProductID": 18,
            "ProductName": "多肉葡萄",
            "Price": 19.9,
            "Description": "鲜嫩多汁的葡萄果肉，搭配清新的茶底，甜而不腻，口感丰富，让人回味无穷。",
            "ImageURL": "https://img.haohan.space/img/202410302225764.png",
            "CreatedDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "CategoryID": 5,
            "CategoryName": "果茶系列",
            "ProductID": 19,
            "ProductName": "椰椰芒芒",
            "Price": 19.9,
            "Description": "浓郁的芒果香甜，融合清爽的椰奶，带来热带风情的味觉享受，清新怡人。",
            "ImageURL": "https://img.haohan.space/img/202410302226754.png",
            "CreatedDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "CategoryID": 5,
            "CategoryName": "果茶系列",
            "ProductID": 20,
            "ProductName": "西瓜波波",
            "Price": 19.9,
            "Description": "新鲜的西瓜汁搭配Q弹的波波球，清凉解暑，夏日必备的消暑佳品。",
            "ImageURL": "https://img.haohan.space/img/202410302227124.png",
            "CreatedDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "CategoryID": 5,
            "CategoryName": "果茶系列",
            "ProductID": 21,
            "ProductName": "杨枝甘露",
            "Price": 19.9,
            "Description": "经典港式甜品，芒果、西柚与椰奶的完美结合，酸甜可口，令人难以忘怀。",
            "ImageURL": "https://img.haohan.space/img/202410302227121.png",
            "CreatedDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        # 其他饮品系列
        {
            "CategoryID": 6,
            "CategoryName": "其他饮品系列",
            "ProductID": 22,
            "ProductName": "纯牛奶",
            "Price": 9.9,
            "Description": "精选高品质纯牛奶，口感醇厚，富含丰富营养，是日常补充能量的理想选择。",
            "ImageURL": "https://img.haohan.space/img/202410302228935.png",
            "CreatedDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "CategoryID": 6,
            "CategoryName": "其他饮品系列",
            "ProductID": 23,
            "ProductName": "黑巧",
            "Price": 12.9,
            "Description": "浓郁的黑巧克力饮品，微苦中带甜，满足您对纯正可可的渴望，带来极致享受。",
            "ImageURL": "https://img.haohan.space/img/202410302228655.png",
            "CreatedDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        # 小食系列
        {
            "CategoryID": 7,
            "CategoryName": "小食系列",
            "ProductID": 24,
            "ProductName": "火腿三明治",
            "Price": 12.9,
            "Description": "新鲜的面包夹着优质火腿和新鲜蔬菜，简单却美味，补充能量的最佳选择。",
            "ImageURL": "https://img.haohan.space/img/202410302229777.png",
            "CreatedDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "CategoryID": 7,
            "CategoryName": "小食系列",
            "ProductID": 25,
            "ProductName": "培根蛋堡",
            "Price": 15.9,
            "Description": "酥软的面包内夹着香脆的培根和嫩滑的煎蛋，口感丰富，满足您的味蕾。",
            "ImageURL": "https://img.haohan.space/img/202410302230278.png",
            "CreatedDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "CategoryID": 7,
            "CategoryName": "小食系列",
            "ProductID": 26,
            "ProductName": "芝士蛋糕",
            "Price": 16.9,
            "Description": "浓郁的芝士风味，口感细腻绵软，甜而不腻，是甜品爱好者的不二之选。",
            "ImageURL": "https://img.haohan.space/img/202410302230898.png",
            "CreatedDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "CategoryID": 7,
            "CategoryName": "小食系列",
            "ProductID": 27,
            "ProductName": "巧克力曲奇",
            "Price": 4.9,
            "Description": "酥脆可口的巧克力曲奇，浓浓的巧克力香气，搭配咖啡或茶更是绝佳选择。",
            "ImageURL": "https://img.haohan.space/img/202410302230731.png",
            "CreatedDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
    ]
    # 插入数据
        insert_sql = '''
    INSERT INTO products (CategoryID, CategoryName, ProductID, ProductName, Price, Description, ImageURL, CreatedDate)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''
        for product in products:
            cursor.execute(insert_sql, (
                product["CategoryID"],
                product["CategoryName"],
                product["ProductID"],
                product["ProductName"],
                product["Price"],
                product["Description"],
                product["ImageURL"],
                product["CreatedDate"]
            ))
        connection.commit()

        stock = [
            {
                "ProductID": 1,
                "Stock": 100
            },
            {
                "ProductID": 2,
                "Stock": 100
            },
            {
                "ProductID": 3,
                "Stock": 100
            },
            {
                "ProductID": 4,
                "Stock": 100
            },
            {
                "ProductID": 5,
                "Stock": 100
            },
            {
                "ProductID": 6,
                "Stock": 100
            },
            {
                "ProductID": 7,
                "Stock": 100
            },
            {
                "ProductID": 8,
                "Stock": 100
            },
            {
                "ProductID": 9,
                "Stock": 100
            },
            {
                "ProductID": 10,
                "Stock": 100
            },
            {
                "ProductID": 11,
                "Stock": 100
            },
            {
                "ProductID": 12,
                "Stock": 100
            },
            {
                "ProductID": 13,
                "Stock": 100
            },
            {
                "ProductID": 14,
                "Stock": 100
            },
            {
                "ProductID": 15,
                "Stock": 100
            },
            {
                "ProductID": 16,
                "Stock": 100
            },
            {
                "ProductID": 17,
                "Stock": 100
            },
            {
                "ProductID": 18,
                "Stock": 100
            },
            {
                "ProductID": 19,
                "Stock": 100
            },
            {
                "ProductID": 20,
                "Stock": 100
            },
            {
                "ProductID": 21,
                "Stock": 100
            },
            {
                "ProductID": 22,
                "Stock": 100
            },
            {
                "ProductID": 23,
                "Stock": 100
            },
            {
                "ProductID": 24,
                "Stock": 100
            },
            {
                "ProductID": 25,
                "Stock": 100
            },
            {
                "ProductID": 26,
                "Stock": 100
            },
            {
                "ProductID": 27,
                "Stock": 100
            }
        ]
        insert_stock_sql = '''

    INSERT INTO product_stock (ProductID, Stock)
    VALUES (%s, %s)
    '''
        for s in stock:
            cursor.execute(insert_stock_sql, (
                s["ProductID"],
                s["Stock"]
            ))
        connection.commit()
        print("数据插入成功")
    
except Exception as e:
    print(f"发生错误：{e}")
    connection.rollback()
finally:
    connection.close()