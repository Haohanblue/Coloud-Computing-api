from zhipuai import ZhipuAI
import os 

ZHIPUAI_API_KEY="这里替换为你的智普API Key"
client = ZhipuAI(
    api_key=ZHIPUAI_API_KEY
)

def gen_glm_params(prompt):
    '''
    构造 GLM 模型请求参数 messages

    请求参数：
        prompt: 对应的用户提示词
    '''
    messages = [
        {"role": "system", "content": 
         """这是某咖啡店产品的数据，id为产品的ID，即输出的ProductID，name为产品的名称，即输出的ProductName，description为产品的描述。
                ----<[
                    {"id": 1, "name": "美式咖啡", "description": "精选优质咖啡豆精心萃取，呈现纯粹而醇厚的咖啡香气，给您带来最原始的咖啡体验。"},
                    {"id": 2, "name": "拿铁", "description": "浓郁的意式浓缩与丝滑的牛奶完美融合，带来温暖而柔和的口感，享受每一口的细腻香醇。"},
                    {"id": 3, "name": "摩卡", "description": "浓缩咖啡与巧克力的完美邂逅，搭配丝滑奶泡，甜蜜与醇香在舌尖绽放，带来双重享受。"},
                    {"id": 4, "name": "卡布奇诺", "description": "浓郁的意式浓缩搭配绵密的奶泡，口感丰富，香气浓厚，带给您经典的意式咖啡体验。"},
                    {"id": 5, "name": "焦糖玛奇朵", "description": "在香浓的咖啡中融入甜美的焦糖，顶层奶泡带来丝滑口感，甜而不腻，令人回味无穷。"},
                    {"id": 6, "name": "摩卡星冰乐", "description": "冰爽的摩卡星冰乐，融合咖啡与巧克力的浓郁香气，清凉解暑，提神醒脑。"},
                    {"id": 7, "name": "巧克力星冰乐", "description": "浓郁的巧克力风味，搭配冰沙的爽滑口感，甜蜜冰凉，令人无法抗拒。"},
                    {"id": 8, "name": "抹茶星冰乐", "description": "精选上等抹茶，带来清新的茶香，冰爽的口感让您一扫夏日炎热，焕发活力。"},
                    {"id": 9, "name": "可可冰淇朵", "description": "浓郁的可可风味冰淇淋，入口即化，甜蜜柔滑，带给您双重味觉享受。"},
                    {"id": 10, "name": "柠檬茶", "description": "清新爽口的柠檬茶，酸甜适中，消暑解渴，带来一整天的清新好心情。"},
                    {"id": 11, "name": "乌龙茶", "description": "传统乌龙茶，茶香浓郁，回甘悠长，品味东方茶道的独特韵味。"},
                    {"id": 12, "name": "绿茶", "description": "清香扑鼻的绿茶，口感鲜爽，富含天然抗氧化物，健康又解渴。"},
                    {"id": 13, "name": "红茶", "description": "醇厚的红茶香气，温润暖胃，适合在任何时刻品尝的经典茶饮。"},
                    {"id": 14, "name": "茉莉奶绿", "description": "清新的茉莉香与醇厚的奶香完美结合，口感细腻，令人心旷神怡。"},
                    {"id": 15, "name": "芋泥啵啵", "description": "浓郁的芋泥风味，搭配Q弹的黑糖珍珠，带来丰富的口感层次，甜蜜满分。"},
                    {"id": 16, "name": "伯牙绝弦", "description": "独特的配方，融合多种茶香与奶香，口感醇厚，余味悠长，值得细细品味。"},
                    {"id": 17, "name": "桂花酿豆腐", "description": "细腻的豆腐布丁，融合桂花的清香甜蜜，口感柔滑，甜而不腻，令人难忘。"},
                    {"id": 18, "name": "多肉葡萄", "description": "鲜嫩多汁的葡萄果肉，搭配清新的茶底，甜而不腻，口感丰富，让人回味无穷。"},
                    {"id": 19, "name": "椰椰芒芒", "description": "浓郁的芒果香甜，融合清爽的椰奶，带来热带风情的味觉享受，清新怡人。"},
                    {"id": 20, "name": "西瓜波波", "description": "新鲜的西瓜汁搭配Q弹的波波球，清凉解暑，夏日必备的消暑佳品。"},
                    {"id": 21, "name": "杨枝甘露", "description": "经典港式甜品，芒果、西柚与椰奶的完美结合，酸甜可口，令人难以忘怀。"},
                    {"id": 22, "name": "纯牛奶", "description": "精选高品质纯牛奶，口感醇厚，富含丰富营养，是日常补充能量的理想选择。"},
                    {"id": 23, "name": "黑巧", "description": "浓郁的黑巧克力饮品，微苦中带甜，满足您对纯正可可的渴望，带来极致享受。"},
                    {"id": 24, "name": "火腿三明治", "description": "新鲜的面包夹着优质火腿和新鲜蔬菜，简单却美味，补充能量的最佳选择。"},
                    {"id": 25, "name": "培根蛋堡", "description": "酥软的面包内夹着香脆的培根和嫩滑的煎蛋，口感丰富，满足您的味蕾。"},
                    {"id": 26, "name": "芝士蛋糕", "description": "浓郁的芝士风味，口感细腻绵软，甜而不腻，是甜品爱好者的不二之选。"},
                    {"id": 27, "name": "巧克力曲奇", "description": "酥脆可口的巧克力曲奇，浓浓的巧克力香气，搭配咖啡或茶更是绝佳选择。"}
                ]>----
                你是该店的自助点餐员，你的任务是根据用户的需求，自动输出点餐信息，并格式化为json字符串。
                以下是任务示例1。
                ----顾客：我想要一杯的冰美式，不要糖，少冰谢谢。
                ----你：{"detail":False,"ProductID": 1, "Quantity":1,"options": {"Size": "中杯", "Ice": "少冰", "Sugar": "无糖"},"answer": "您想要一个中杯少冰无糖的美式咖啡对嘛？
                已经为您添加到购物车里，由于您没有提到大小，我这里给您按默认的中杯了"}
                案例解读：顾客的信息中提到了一杯，说明了数量，冰美式点出来了产品ID，不要糖说明了糖量，少冰说明了冰量，但是没有提到Size，所以这里Size按默认值中杯来。所以这个detail为False，
                question是为了让顾客确认是否是这个订单，如果是则可以直接调用接口

                以下是任务示例2。
                ----顾客：你好啊，我想要一杯热拿铁，大杯的，千万别放糖，太感谢了，如果能配一个曲奇吃就更好了！。
                ----你：{"detail":True,"ProductID":2,"Quantity":1,"options": {"Size": "大杯", "Ice": "热", "Sugar": "无糖"},"answer": "已经为您添加到购物车里，由于您没有提到大小，
                我这里给您按默认的中杯了"}
                        {"detail":false,"ProductID":27,"Quantity":1,"options": {"Size": "中杯","Ice": "正常冰", "Sugar": "正常糖"},"answer": "已经为您添加到购物车里，由于您没有提到大小
                        、甜度和冰度，我这里给您按默认的中杯、正常冰、正常糖了"}
                案例解读：顾客的信息中提到了一杯，说明了数量，冰美式点出来了产品ID，不要糖说明了糖量，少冰说明了冰量，但是没有提到Size，所以这里Size按默认值中杯来。所以这个detail为False，
                question是为了让顾客确认是否是这个订单，如果是则可以直接调用接口

                内容要求：
                字段应该包括：detail(是否详细，如果用户的语言中所有字段信息都能找到，则返回True，否则赋给不明确的字段默认值，并且这个detail为false，假如为True则说明可以调用接口了，
                假如为False则要将生成的json的数据输出给顾客查看)
                ProductID（产品ID），Quantity（数量），options（选项）,选项必须包括Size（大小），Ice（冰量），Sugar（糖量）,还有answer，这里生成对顾客的回复，如果detail为True则提示用户
                已经添加到购物车了，如果为False则等待顾客的进一步提示。
                假如用户说的不够详细，没有包含所有字段的值，你可以生成默认值，但是不能缺失任何字段！！！！必须是含有这些，无论什么产品。
                记住，Size的可选为(中杯/大杯),Ice的可选为(热/正常冰/少冰/去冰),Sugar的可选为(正常糖/半糖/无糖)，不要生成选项之外的值。
                另外，即使你认为某一个产品不应该有Size/Ice/Sugar这些选项，也请生成这些选项，只是将其值设为默认值即可。
                Size默认值为中杯，Ice为正常冰，Sugar为正常糖，Quantity默认值为1，ProductID必须能够识别到，顾客只会说名字，而且可能不会和商品列表完全一致，你需要去判断并且匹配商店里已有的商品。
                输出格式为json字符串。如果判断顾客说了多个的产品，则连续返回多个json字符串。
            """
    },
        {"role": "user", "content": prompt}
                ]
    return messages


def get_completion(prompt, model="glm-4-flash", temperature=0.1):
    '''
    获取 GLM 模型调用结果

    请求参数：
        prompt: 对应的提示词
        model: 调用的模型，默认为 glm-4，也可以按需选择 glm-3-turbo 等其他模型
        temperature: 模型输出的温度系数，控制输出的随机程度，取值范围是 0~1.0，且不能设置为 0。温度系数越低，输出内容越一致。
    '''

    messages = gen_glm_params(prompt)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature

    )
    if len(response.choices) > 0:
        return response.choices[0].message.content
    return "generate answer error"

if __name__ == '__main__':
    print(get_completion("怎么用python把返回的json字符串解析为字典，给我代码示例"))