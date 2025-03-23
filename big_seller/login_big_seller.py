import base64
import json

import ddddocr
import requests
from io import BytesIO
from PIL import Image


def base64_to_img(base64_str):
    head, context = base64_str.split(",")  # 将base64_str以“,”分割为两部分
    img_data = base64.b64decode(context)  # 解码时只要内容部分

    return Image.open(BytesIO(img_data))


def do_login(id=""):
    # 获取验证码
    verify_url = "https://www.bigseller.com/api_v2/api/v2/genVerifyCode.json"
    request_res = requests.get(
        url=verify_url,
    )
    result = json.loads(request_res.text).get("data")
    # 识别验证码
    ocr = ddddocr.DdddOcr()
    verifyCode_result = ocr.classification(base64_to_img(result.get("base64Image")))
    # 登录流程
    login_url = "https://www.bigseller.com/api_v2/api/v2/user/login.json"
    login_result = requests.post(
        headers={
            # "user-agent": UserAgent().random,
            "Host": "www.bigseller.com",
            "Connection": "keep-alive",
            "Content-Length": 185,
            "sec-ch-ua-platform": "macOS",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "accept": "application/json",
            "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "content-type": "application/x-www-form-urlencoded",
            "sec-ch-ua-mobile": "?0",
            "Origin": "https://www.bigseller.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://www.bigseller.com/zh_CN/login.htm?redirect=https://www.bigseller.com/web/listing/shopeeGlobal/draft.htm",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7"
        },
        url=login_url,
        data=f"email={id}&password=058d4ec5a67eeac363cb8b080a52e95ec6629906199d1a9ddfc89727caf53f69c090402f1c4c8b1d1091e610a64f1211b145c&verifyCode={verifyCode_result}&accessCode={result.get('accessCode')}")
    print(login_result.text)
    return login_result.text


if __name__ == '__main__':
    do_login("liudewei0616%40gmail.com")
