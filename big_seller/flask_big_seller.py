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
    resultStr = ''
    data = request_parse(request)
    user_id = data.get("userId")
    bs_status = data.get("bsStatus")
    shop_id = data.get("shopId")
    page_no = data.get("pageNo")
    page_size = data.get("pageSize")
    inquire_type = data.get("inquireType")
    search_type = data.get("searchType")
    search_content = data.get("searchContent")

    if user_id:
        url = "https://www.bigseller.com/api/v1/product/global/shopee/draft.json"
        current_cookie = next(v['cookie'] for v in g.user_list if v['id'] == user_id)
        if current_cookie:
            headers = {"Cookie": current_cookie.strip()}
            params = {
                "bsStatus": bs_status,
                "shopId": shop_id,
                "pageNo": page_no,
                "pageSize": page_size,
                "inquireType": inquire_type,
                "searchType": search_type,
                "searchContent": search_content,
            }
            request_res = requests.get(url=url, params=params, headers=headers)
            resultStr = response_parse(request_res.text)
        else:
            resultStr = response_parse("token不存在！！！", is_success=False)
    else:
        resultStr = response_parse("用户id不存在！！！", is_success=False)
    return resultStr

# 获取在线产品列表
@app.route("/getBigSellerOnLineProduct", methods=["GET", "POST"])
def getBigSellerOnLineProduct():
    resultStr = ''
    data = request_parse(request)
    user_id = data.get("userId")
    bs_status = data.get("bsStatus")
    shop_id = data.get("shopId")
    page_no = data.get("pageNo")
    page_size = data.get("pageSize")
    inquire_type = data.get("inquireType")
    search_type = data.get("searchType")
    search_content = data.get("searchContent")

    if user_id:
        url = "https://www.bigseller.com/api/v1/product/global/shopee/active.json"
        current_cookie = next(v['cookie'] for v in g.user_list if v['id'] == user_id)
        if current_cookie:
            headers = {"Cookie": current_cookie.strip()}
            params = {
                "bsStatus": bs_status,
                "shopId": shop_id,
                "pageNo": page_no,
                "pageSize": page_size,
                "inquireType": inquire_type,
                "searchType": search_type,
                "searchContent": search_content,
            }
            request_res = requests.get(url=url, params=params, headers=headers)
            resultStr = response_parse(request_res.text)
        else:
            resultStr = response_parse("token不存在！！！", is_success=False)
    else:
        resultStr = response_parse("用户id不存在！！！", is_success=False)
    return resultStr


if __name__ == "__main__":
    app.run("127.0.0.1", 9980, debug=False)
