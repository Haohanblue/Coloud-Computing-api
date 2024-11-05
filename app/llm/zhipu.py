import llm
import json
def get_completion(prompt):
    return llm.get_completion(prompt)

def zhipu(prompt:str):
    res = get_completion(prompt)
    cleaned_json_str = res.replace("```json", "", 1).replace("```", "", 1).strip()
    response = json.loads(cleaned_json_str)
    if type(response) == dict:
        data = {
            "ProductID":response["ProductID"],
            "Quantity":response["Quantity"],
            "Size":response["options"]["Size"],
            "Ice":response["options"]["Ice"],
            "Sugar":response["options"]["Sugar"],
        }
    elif type(response) == list:
        data = []
        for i in response:
            data.append({
                "ProductID":i["ProductID"],
                "Quantity":i["Quantity"],
                "Size":i["options"]["Size"],
                "Ice":i["options"]["Ice"],
                "Sugar":i["options"]["Sugar"],
            })
    print("用户的提问:",prompt)
    print("大模型生成的回复:",response)
    print("经过转换要提交给接口的请求体:",data)
    return data
zhipu("我想要一杯的冰美式，不要糖，少冰谢谢。")
zhipu("两杯拿铁，一杯热的，一杯冰的，都不要糖，对了，还有一个曲奇")
zhipu("今天真冷啊，来一杯美式吧")
zhipu("刚跑完步，太热啦，想喝柠檬水")