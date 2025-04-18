import base64
import json
from urllib import parse

from flask import Flask, g, request

from spider_big_seller import BigSellerLogin
from flask_cors import CORS
import urllib.request
import urllib.parse
from fake_useragent import UserAgent
import ddddocr
from io import BytesIO
from PIL import Image

app = Flask(__name__)
CORS(app, resources=r'/*', supports_credentials=True)


def request_parse(req_data):
    """解析请求数据并以json形式返回"""
    global data
    if req_data.method == 'POST':
        data = req_data.json
    elif req_data.method == 'GET':
        data = req_data.args
    return data


def response_parse(resp_str, is_success=True, need_load=True):
    if is_success:
        return json.dumps({
            "code": 200,
            "data": json.loads(resp_str) if need_load is True else resp_str
        })
    else:
        return json.dumps({
            "code": 500,
            "msg": resp_str
        })


# request 获取参数
def get_request_params(param_list=None, info_list=None):
    if param_list is None:
        param_list = []
    if info_list is None:
        info_list = []
    request_data = request_parse(request)
    result_obj = {
        "cookie": "",
        "params": {},
        "info": {},
        "is_success": False,
    }
    userId = request_data.get("userId")
    if userId:
        current_cookie = next(v['cookie'] for v in g.user_list if v['id'] == userId)
        current_cookie_str = ""
        for k, v in current_cookie.items():
            current_cookie_str += "%s=%s; " % (k, v)
        if current_cookie:
            result_obj["cookie"] = current_cookie_str
            if len(param_list) != 0:
                for param in param_list:
                    result_obj["params"][param] = request_data.get(param)
            if len(info_list) != 0:
                for info in info_list:
                    result_obj["info"][info] = request_data.get(info)
            result_obj["is_success"] = True
    return result_obj


def get_error_text():
    return response_parse("用户id或者token不存在！！！", is_success=False)


@app.before_request
def before_request():
    # 在请求之前设置g对象的数据
    with open('/Users/个人/电商/电商后台/big_seller/accountToken.json', 'r', encoding='utf-8') as f:
        g.user_list = json.loads(f.read())


# 获取账号列表
@app.route("/getBigSellerUserList", methods=["GET", "POST"])
def getBigSellerUserList():
    resultStr = response_parse(
        [
            {
                "id": item.get("id"),
                "shopId": item.get("shopId"),
                "name": item.get("name"),
                "password": item.get("password"),
                "muc_token": item["cookie"]["muc_token"],
            } for item in g.user_list
        ],
        need_load=False)
    return resultStr


# 获取产品列表
@app.route("/getBigSellerShopList", methods=["GET", "POST"])
def getBigSellerShopList():
    param_obj = get_request_params(["userId"])
    url = "https://www.bigseller.com/api/v1/shop/getPermissionShops.json"
    if param_obj["is_success"] is True:
        resultStr = proxy_open(url, method="POST", data={"platform": "shopee"}, headers={"Cookie": param_obj["cookie"]})
    else:
        resultStr = get_error_text()
    return resultStr


# 获取产品列表
@app.route("/getBigSellerList", methods=["GET", "POST"])
def getBigSellerList():
    param_obj = get_request_params([
        "status",
        "pageNo",
        "pageSize",
        "inquireType",
        "searchType",
        "desc",
        "orderBy",
        "searchContent",
        "shopId"
    ])
    if param_obj['params']['status'] == 'collect':
        url = "https://www.bigseller.com/api/v1/product/crawl/pageList.json"
    else:
        url = f'https://www.bigseller.com/api/v1/product/listing/shopee/{param_obj["params"]["status"]}.json?orderBy={param_obj["params"]["orderBy"]}&desc={param_obj["params"]["desc"]}&searchType={param_obj["params"]["searchType"]}&inquireType={param_obj["params"]["inquireType"]}&status={param_obj["params"]["status"]}&pageNo={param_obj["params"]["pageNo"]}&pageSize={param_obj["params"]["pageSize"]}&shopId={param_obj["params"]["shopId"]}'
    if param_obj["is_success"] is True:
        resultStr = proxy_open(url, headers={"Cookie": param_obj["cookie"]})
    else:
        resultStr = get_error_text()
    return resultStr


# 获取是否登录
@app.route("/getBigSellerIsLogin", methods=["GET", "POST"])
def getBigSellerIsLogin():
    url = "https://www.bigseller.com/api/v1/isLogin.json"
    param_obj = get_request_params(["userId"])
    if param_obj["is_success"] is True:
        resultStr = proxy_open(url, data=param_obj["params"], headers={"Cookie": param_obj["cookie"]})
        resultJson = json.loads(resultStr)
        if resultJson["data"] is False:
            print("执行重新登录！！！")
            bigSeller = BigSellerLogin()
            driver = bigSeller.open_browser()
            result_obj = bigSeller.go_bigSeller(driver)
            if result_obj["result"] is True:
                g.user_list = result_obj["user_list"]
                param_obj = get_request_params(["userId"])
                if param_obj["is_success"] is True:
                    resultStr = proxy_open(url, data=param_obj["params"], headers={"Cookie": param_obj["cookie"]})
            else:
                print("需要重新登录！！！")
    else:
        resultStr = get_error_text()
    return resultStr


# 获取详情页
@app.route("/getBigSellerEditDetail", methods=["GET", "POST"])
def getBigSellerEditDetail():
    param_obj = get_request_params(["userId"], info_list=["id"])
    if param_obj["is_success"] is True:
        url = f'https://www.bigseller.com/api/v1/product/listing/shopee/edit/{param_obj["info"]["id"]}.json'
        resultStr = proxy_open(url, data=param_obj["params"], headers={"Cookie": param_obj["cookie"]})
    else:
        resultStr = get_error_text()
    return resultStr


# 修改详情页
@app.route("/editBigSellerShopee", methods=["GET", "POST"])
def editBigSellerShopee():
    url = "https://www.bigseller.com/api/v1/product/listing/shopee/edit.json"
    param_obj = get_request_params([
        "editObj"
    ])
    data_obj = {}
    filter_params = ["id", "shopId", "name", "itemSku", "originalPrice", "stock", "variations", "discountId",
                     "categoryId", "option1", "option2", "images", "weight", "daysToShip", "gtinCode", "productExtra",
                     "productText", "operate"]
    edit_obj = json.loads(param_obj["params"]["editObj"])
    for param_item in filter_params:
        data_obj[param_item] = edit_obj.get(param_item)
    if param_obj["is_success"] is True:
        resultStr = proxy_open(url, method="POST", data=data_obj,
                               headers={"Cookie": param_obj["cookie"]}, is_json=True)
    else:
        resultStr = get_error_text()
    return resultStr


# 图片换源
@app.route("/changeBigSellerImgSource", methods=["GET", "POST"])
def changeBigSellerImgSource():
    url = "https://www.bigseller.com/api/v1/product/listing/shopee/changeShopeeMd5.json"
    param_obj = get_request_params([
        "id",
        "img",
        "watermark"
    ])
    if param_obj["is_success"] is True:
        resultStr = proxy_open(url, method="POST", data=param_obj["params"], headers={"Cookie": param_obj["cookie"]})
    else:
        resultStr = get_error_text()
    return resultStr


# 图片换源后检查是否成功
@app.route("/checkImgSourceTask", methods=["GET", "POST"])
def checkImgSourceTask():
    url = "https://www.bigseller.com/api/v1/product/listing/shopee/md5/check.json"
    param_obj = get_request_params([
        "operateKey",
    ])
    if param_obj["is_success"] is True:
        resultStr = proxy_open(url, method="POST", data=param_obj["params"], headers={"Cookie": param_obj["cookie"]})
    else:
        resultStr = get_error_text()
    return resultStr


@app.route("/doLogin", methods=["GET"])
def doLogin(id=""):
    return do_login(id)


def proxy_open(url, method="GET", data={}, headers={}, is_json=False):
    if data is None:
        data = {}
    proxy = urllib.request.ProxyHandler(
        {'http': 'customer-najJ5b6tFD-cc-HK-sessid-1742724200_10007:aAy5zvLV4F3cr2D@gate-sg.ipfoxy.io:58688'})
    auth = urllib.request.HTTPBasicAuthHandler()
    opener = urllib.request.build_opener(proxy, auth, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    req_headers = {**get_dynamic_headers(is_json), **headers}
    if is_json:
        request_data = json.dumps(data).encode('utf-8')
    else:
        request_data = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(url=url, headers=req_headers, data=request_data, method=method)
    # 发送请求并获取响应
    with urllib.request.urlopen(req) as response:
        result = response.read().decode('utf-8')  # 将响应内容转为字符串
    return result


def get_dynamic_headers(is_json=False):
    # 初始化 UserAgent 对象（自动缓存最新数据）
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        "Referer": "https://www.bigseller.com/",
        "Connection": "keep-alive"
    }
    if is_json:
        headers["Content-Type"] = "application/json;charset=UTF-8"
    return headers


def base64_to_img(base64_str):
    head, context = base64_str.split(",")  # 将base64_str以“,”分割为两部分
    img_data = base64.b64decode(context)  # 解码时只要内容部分

    return Image.open(BytesIO(img_data))


def do_login(id=""):
    # 获取验证码
    verify_content = proxy_open("https://www.bigseller.com/api_v2/api/v2/genVerifyCode.json")
    verify_result = json.loads(verify_content).get("data")
    # 识别验证码
    ocr = ddddocr.DdddOcr()
    verifyCode_result = ocr.classification(base64_to_img(verify_result.get("base64Image")))
    # 登录流程
    login_url = "https://www.bigseller.com/api_v2/api/v3/auth/loginsub.json"
    # todo password 是实时更新的，待确认更新方法 2025/03/26
    login_request_data = {
        "account": id,
        "password": "06b2b862d729915cc0a05394f3361ff2a5aacfdeb62895ef89bbe60483097616c2d269bdb512d4ed60bb5e4d70609a551b739",
        "accessCode": verify_result.get('accessCode'),
        "picVerificationCode": verifyCode_result,
        "phoneAccountCode": "undefined"
    }
    login_result = proxy_open(login_url, method="POST", data=login_request_data)
    print(login_result, "tttttt")
    return login_result


if __name__ == "__main__":
    app.run("0.0.0.0", port=9980, debug=False)
    # tes_proxy()
