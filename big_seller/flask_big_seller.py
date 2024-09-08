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


@app.before_request
def before_request():
    # 在请求之前设置g对象的数据
    with open('accountToken.json', 'r', encoding='utf-8') as f:
        g.cookie_list = json.loads(f.read())


# 获取账号列表
@app.route("/getBigSellerUserList", methods=["GET", "POST"])
def getBigSellerUserList():
    resultStr = response_parse(
        [
            {
                "id": item.get("id"),
                "name": item.get("name")
            } for item in g.cookie_list
        ],
        need_load=False)
    return resultStr


# 获取草稿箱列表
@app.route("/getBigSellerDraftBox", methods=["GET", "POST"])
def getBigSellerDraftBox():
    resultStr = ''
    data = request_parse(request)
    user_id = data.get("userId")

    if user_id:
        url = "https://www.bigseller.com/api/v1/product/global/shopee/draft.json?bsStatus=1&shopId=&pageNo=1&pageSize=50"
        current_cookie = next(v['cookie'] for v in g.cookie_list if v['id'] == user_id)
        if current_cookie:
            headers = {"Cookie": current_cookie.strip()}
            request_res = requests.get(url=url, headers=headers)
            resultStr = response_parse(request_res.text)
        else:
            resultStr = response_parse("token不存在！！！", is_success=False)
    else:
        resultStr = response_parse("用户id不存在！！！", is_success=False)
    return resultStr


if __name__ == "__main__":
    app.run("127.0.0.1", 9980, debug=False)
