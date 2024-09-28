import base64
import json
import requests
from io import BytesIO
from PIL import Image
from cnocr import CnOcr


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
    img_data = base64_to_img(result.get("base64Image"))
    ocr = CnOcr(cand_alphabet="0123456789AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz")
    verifyCode_result = ocr.ocr(img_data)[0].get("text")
    # 登录流程
    login_url = "https://www.bigseller.com/api_v2/api/v2/user/login.json"
    login_result = requests.post(
        url=login_url,
        data=f"email={id}&password=058d4ec5a67eeac363cb8b080a52e95ec6629906199d1a9ddfc89727caf53f69c090402f1c4c8b1d1091e610a64f1211b145c&verifyCode={verifyCode_result}&accessCode={result.get('accessCode')}")
    print(login_result.text)
    return login_result.text


if __name__ == '__main__':
    do_login("liudewei0616%40gmail.com")
