# -*- coding: utf-8 -*-
'''  
 主题：阿狸pay用户支付签名
 作者：Tommy
 日期：2022年-10月-11日

 注意：User-Agent要设置
'''
import requests
import hashlib

def DO_AlyPay(para_list):

    partner= "1308"
    key= "g525s80e05E5LSmXlyyS72Yc5Sl55S58"
    notify_url= "http://www.pay.com/notify_url.php"
    return_url= "http://www.pay.com/return_url.php"
    sitename = 'MYWEB.COM'
    
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

    if code != 1:
        return {"ret": response_text['code']}

    return payurl


if __name__ == "__main__":
    para_list = {
            "type" : "alipay",
            "out_trade_no"	: "124",
            "name"	: "星冰乐",
            "money"	: "0.01",
            "clientip"	: "192.168.1.100",
            "device" : "jump"
    }
    result = DO_AlyPay(para_list)
    print(result)