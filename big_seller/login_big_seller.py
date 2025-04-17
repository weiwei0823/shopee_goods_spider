import base64
import json

import ddddocr
import requests
from io import BytesIO
from PIL import Image

from urllib import request, parse
import requests
import socks
import socket
from big_seller.flask_big_seller import proxy_open, do_login
from selenium import webdriver

def base64_to_img(base64_str):
    head, context = base64_str.split(",")  # 将base64_str以“,”分割为两部分
    img_data = base64.b64decode(context)  # 解码时只要内容部分

    return Image.open(BytesIO(img_data))


def do_login1(id=""):
    # 获取验证码
    proxy = request.ProxyHandler(
        {'http': 'customer-najJ5b6tFD-cc-HK-sessid-1742724200_10007:aAy5zvLV4F3cr2D@gate-sg.ipfoxy.io:58688'})
    auth = request.HTTPBasicAuthHandler()
    opener = request.build_opener(proxy, auth, request.HTTPHandler)
    request.install_opener(opener)
    verify_content = request.urlopen("https://www.bigseller.com/api_v2/api/v2/genVerifyCode.json").read().decode(
        'utf-8')
    result = json.loads(verify_content).get("data")
    # 识别验证码
    ocr = ddddocr.DdddOcr()
    verifyCode_result = ocr.classification(base64_to_img(result.get("base64Image")))
    print(verifyCode_result)
    # 登录流程
    login_url = "https://www.bigseller.com/api_v2/api/v3/auth/loginsub.json"
    request_data = {
        "account": id,
        "password": "06b2b862d729915cc0a05394f3361ff2a5aacfdeb62895ef89bbe60483097616c2d269bdb512d4ed60bb5e4d70609a551b739",
        "accessCode": result.get('accessCode'),
        "picVerificationCode": verifyCode_result,
        "phoneAccountCode": "undefined"
    }
    headers = {
        "Host": "www.bigseller.com",
        "Connection": "keep-alive",
        "Content-Length": "243",
        "sec-ch-ua-platform": "macOS",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "accept": "application/json",
        "sec-ch-ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        "content-type": "application/json",
        "sec-ch-ua-mobile": "?0",
        "Origin": "https://www.bigseller.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.bigseller.com/zh_CN/login.htm",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        "Cookie": "i18n_redirected=zh_CN; __lt__cid=4e51a77a-7a36-4178-be33-b93b31f4d28d; _hjSessionUser_3051954=eyJpZCI6IjcwODEwNDY1LWM5ODgtNWM1NS1hNDk2LTQxZjUzMTMyZDgzMiIsImNyZWF0ZWQiOjE3MjI4MjM4NTI0NzYsImV4aXN0aW5nIjp0cnVlfQ==; _tt_enable_cookie=1; _ati=7194670310392; MYJ_yosu7anwoc=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJiZWMxNjcyMy1lODRlLTQ5ODQtYjdhMC1hNTJiMTExMjFjMzglMjIlMkMlMjJ1c2VySWQlMjIlM0E5NDE2MjglMkMlMjJwYXJlbnRJZCUyMiUzQTk0MTYyOCUyQyUyMnNlc3Npb25JZCUyMiUzQTE3MjY5ODEyOTMwMzYlMkMlMjJvcHRPdXQlMjIlM0FmYWxzZSUyQyUyMmxhc3RFdmVudFRpbWUlMjIlM0ExNzI2OTgxMzE2MzM1JTJDJTIybGFzdEV2ZW50SWQlMjIlM0EzOSU3RA==; language=zh_CN; _fbp=fb.1.1738545641748.224170500147452344; muc_login_account_type=EMAIL_ACCOUNT_TYPE; _ttp=CnQgHQs6X-jXpuin5EkKCtuNNXf.tt.1; org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE=zh_CN; _ga=GA1.2.42360792.1722823852; _ga_B12GTDKJ1Q=GS1.1.1742442982.24.0.1742442994.0.0.0; _ga_CMT5216T6L=GS1.1.1742442982.151.0.1742442994.48.0.0; MYJ_MKTG_yosu7anwoc=JTdCJTIycmVmZXJyZXIlMjIlM0ElMjJodHRwcyUzQSUyRiUyRnd3dy5iaWdzZWxsZXIuY29tJTJGJTIyJTJDJTIycmVmZXJyaW5nX2RvbWFpbiUyMiUzQSUyMnd3dy5iaWdzZWxsZXIuY29tJTIyJTdE; __lt__sid=e1106ca2-3ec127f2; _clck=rizwh0%7C2%7Cfuh%7C0%7C1678; _hjSession_3051954=eyJpZCI6IjRmMzI2MjE2LTg2NDItNGU4ZS05MDY5LWVlN2YwZjFhMDE3YyIsImMiOjE3NDI3NzUwMTA4MzksInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; MYJ_yosu7anwoc=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJiZWMxNjcyMy1lODRlLTQ5ODQtYjdhMC1hNTJiMTExMjFjMzglMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjIlMjIlMkMlMjJwYXJlbnRJZCUyMiUzQSUyMiUyMiUyQyUyMnNlc3Npb25JZCUyMiUzQTE3NDI3NzUxMTM3MDYlMkMlMjJvcHRPdXQlMjIlM0FmYWxzZSUyQyUyMmxhc3RFdmVudElkJTIyJTNBMzklN0Q=; JSESSIONID=19C5DB1175DD43AD8910ADACF4B5F3AE; _gcl_au=1.1.60938734.1741770591.442853618.1742775013.1742775122",
    }
    request_data_bytes = parse.urlencode(request_data).encode('utf-8')
    req = request.Request(login_url, headers=headers, data=request_data_bytes, method='POST')
    # 发送请求并获取响应
    with request.urlopen(req) as response:
        result2 = response.read().decode('utf-8')  # 将响应内容转为字符串
        print(result2)
    return result2


def tes_proxy():
    test_url = "http://httpbin.org/ip"
    proxies = {
        # "http": "socks5://gate-sg.ipfoxy.io:58688:customer-najJ5b6tFD-cc-US-sessid-1743232597_10017:aAy5zvLV4F3cr2D",
        "http": "http://customer-najJ5b6tFD-cc-US-sessid-1743236714_10031:aAy5zvLV4F3cr2D:gate-sg.ipfoxy.io:58688",
        "https": "https://customer-najJ5b6tFD-cc-US-sessid-1743236714_10031:aAy5zvLV4F3cr2D:gate-sg.ipfoxy.io:58688",
        # "https": "socks5://gate-sg.ipfoxy.io:58688:customer-najJ5b6tFD-cc-US-sessid-1743232597_10017:aAy5zvLV4F3cr2D",
    }
    try:
        test_response = requests.get(test_url, proxies=proxies)
        print("当前 IP:", test_response.json()["origin"])  # 应显示代理服务器的 IP
    except Exception as e:
        print("验证失败:", e)


def do_bigSeller_login():
    webdriver.chrome()

if __name__ == '__main__':
    # res = do_login("liudewei0616@gmail.com")
    # print(tes_proxy())
    a = {
        "a": 1,
        "b": 2,
    }
    print(a.get("c"))
