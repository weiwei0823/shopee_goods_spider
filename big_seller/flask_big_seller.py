import json

from flask import Flask, g, request
import requests

app = Flask(__name__)


def request_parse(req_data):
    '''解析请求数据并以json形式返回'''
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


def get_request_params(param_list=None, info_list=None):
    if param_list is None:
        param_list = []
    if info_list is None:
        info_list = []
    data = request_parse(request)
    result_obj = {
        "cookie": "",
        "params": {},
        "info": {},
        "is_success": False,
    }
    userId = data.get("userId")
    if userId:
        current_cookie = next(v['cookie'] for v in g.user_list if v['id'] == userId)
        current_cookie_str = ""
        for k, v in current_cookie.items():
            current_cookie_str += "%s=%s; " % (k, v)
        if current_cookie:
            result_obj["cookie"] = current_cookie_str
            if len(param_list) != 0:
                for param in param_list:
                    result_obj["params"][param] = data.get(param)
            if len(info_list) != 0:
                for info in info_list:
                    result_obj["info"][info] = data.get(info)
            result_obj["is_success"] = True
    return result_obj


@app.before_request
def before_request():
    # 在请求之前设置g对象的数据
    with open('accountToken.json', 'r', encoding='utf-8') as f:
        g.user_list = json.loads(f.read())


# 获取账号列表
@app.route("/getBigSellerUserList", methods=["GET", "POST"])
def getBigSellerUserList():
    resultStr = response_parse(
        [
            {
                "id": item.get("id"),
                "shopId": item.get("shopId"),
                "name": item.get("name")
            } for item in g.user_list
        ],
        need_load=False)
    return resultStr


# 获取草稿箱列表
@app.route("/getBigSellerDraftBox", methods=["GET", "POST"])
def getBigSellerDraftBox():
    url = "https://www.bigseller.com/api/v1/product/global/shopee/draft.json"
    param_obj = get_request_params([
        "userId",
        "bsStatus",
        "shopId",
        "pageNo",
        "pageSize",
        "inquireType",
        "searchType",
        "searchContent"
    ])
    if param_obj["is_success"] is True:
        request_res = requests.get(
            url=url,
            params=param_obj["params"],
            headers={"Cookie": param_obj["cookie"]}
        )
        resultStr = response_parse(request_res.text)
    else:
        resultStr = response_parse("用户id或者token不存在！！！", is_success=False)
    return resultStr


# 获取在线产品列表
@app.route("/getBigSellerOnLineProduct", methods=["GET", "POST"])
def getBigSellerOnLineProduct():
    url = "https://www.bigseller.com/api/v1/product/global/shopee/active.json"
    param_obj = get_request_params([
        "userId",
        "bsStatus",
        "shopId",
        "pageNo",
        "pageSize",
        "inquireType",
        "searchType",
        "searchContent"
    ])
    if param_obj["is_success"] is True:
        request_res = requests.get(
            url=url,
            params=param_obj["params"],
            headers={"Cookie": param_obj["cookie"]}
        )
        resultStr = response_parse(request_res.text)
    else:
        resultStr = response_parse("用户id或者token不存在！！！", is_success=False)
    return resultStr


# 获取采集区列表
@app.route("/getBigSellerCollectList", methods=["GET", "POST"])
def getBigSellerCollectList():
    url = "https://www.bigseller.com/api/v1/product/crawl/pageList.json"
    param_obj = get_request_params([
        "userId",
        "claimStatus",
        "crawlPlatform",
        "desc",
        "orderBy",
        "pageNo",
        "pageSize",
        "inquireType",
        "searchType",
        "searchContent",
        "site"
    ])
    if param_obj["is_success"] is True:
        request_res = requests.get(
            url=url,
            params=param_obj["params"],
            headers={"Cookie": param_obj["cookie"]}
        )
        resultStr = response_parse(request_res.text)
    else:
        resultStr = response_parse("用户id或者token不存在！！！", is_success=False)
    return resultStr


# 获取是否登录
@app.route("/getBigSellerIsLogin", methods=["GET", "POST"])
def getBigSellerIsLogin():
    url = "https://www.bigseller.com/api/v1/isLogin.json"
    param_obj = get_request_params([])
    if param_obj["is_success"] is True:
        request_res = requests.get(
            url=url,
            params=param_obj["params"],
            headers={"Cookie": param_obj["cookie"]}
        )
        resultStr = response_parse(request_res.text)
    else:
        resultStr = response_parse("用户id或者token不存在！！！", is_success=False)
    return resultStr


# 获取详情页
@app.route("/getBigSellerEditDetail", methods=["GET", "POST"])
def getBigSellerEditDetail():
    param_obj = get_request_params(info_list=["id"])
    if param_obj["is_success"] is True:
        request_res = requests.get(
            url="https://www.bigseller.com/api/v1/product/global/shopee/edit/%s.json" % param_obj["info"]["id"],
            headers={"Cookie": param_obj["cookie"]}
        )
        resultStr = response_parse(request_res.text)
    else:
        resultStr = response_parse("用户id或者token不存在！！！", is_success=False)
    return resultStr


if __name__ == "__main__":
    app.run("127.0.0.1", 9980, debug=False)
