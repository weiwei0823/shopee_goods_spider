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


@app.before_request
def before_request():
    # 在请求之前设置g对象的数据
    with open('accountToken.json', 'r', encoding='utf-8') as f:
        g.cookie_obj = json.loads(f.read())


# 获取账号列表
@app.route("/getBigSellerAccountList", methods=["GET", "POST"])
def getBigSellerAccountList():
    url = "https://www.bigseller.com/api/v1/product/global/shopee/draft.json?bsStatus=1&shopId=&pageNo=1&pageSize=50"
    big_seller_cookies_str = """ZDgzMiIsImNyZWF0ZWQiOjE3MjI4MjM4NTI0NzYsImV4aXN0aW5nIjp0cnVlfQ==; _tt_enable_cookie=1; _ttp=CnQgHQs6X-jXpuin5EkKCtuNNXf; _ati=7194670310392; _ga_B12GTDKJ1Q=GS1.1.1724032548.5.1.1724032569.0.0.0; _ga=GA1.1.42360792.1722823852; MYJ_MKTG_yosu7anwoc=JTdCJTdE; org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE=zh_CN; MYJ_yosu7anwoc=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJiZWMxNjcyMy1lODRlLTQ5ODQtYjdhMC1hNTJiMTExMjFjMzglMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjIlMjIlMkMlMjJwYXJlbnRJZCUyMiUzQSUyMiUyMiUyQyUyMnNlc3Npb25JZCUyMiUzQTE3MjQ1NTI0NzQwNDclMkMlMjJvcHRPdXQlMjIlM0FmYWxzZSUyQyUyMmxhc3RFdmVudElkJTIyJTNBMzUlN0Q=; _gcl_au=1.1.857027223.1722823850.303722612.1725031581.1725031586; _clck=rizwh0%7C2%7Cfou%7C0%7C1678; __lt__sid=e1106ca2-3f25f778; muc_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyIiwiZXhwIjoxNzI3NDA2MjYzLCJpYXQiOjE3MjU2NzgyNjMsImluZm8iOiJ7XCJyZXF1ZXN0SWRcIjpcIm11Y180MGNldjh6eDJ6YmcxazJoaTRcIixcImxvZ2luVGltZVwiOjE3MjQ5NDU3ODcwOTMsXCJyZWZyZXNoVGltZVwiOjE3MjU2NzgyNjM2NjMsXCJwdWlkXCI6OTQxNjI4LFwicmVxdWVzdElwXCI6XCIzNi4xNTkuMTkyLjE4OVwiLFwicmVxdWVzdENsaWVudFwiOlwiRGV2aWNlOkRlc2t0b3B8U3lzdGVtOm1hY09TLDEwLjE1fENsaWVudDpDaHJvbWUsMFwiLFwidWlkXCI6OTQxNjI4LFwicmFuZG9tU3RyXCI6XCI1MGY1YzRlOC1iMTRhLTQwNDAtYWM1Yi01YWM0YzMzNTY4ZGNcIn0ifQ.9G5vRKkUvuXI6P_ceaXQclDN8MPgYepXHV87fE5wPUM; _ga_CMT5216T6L=GS1.1.1725678264.42.1.1725678279.45.0.0; MYJ_yosu7anwoc=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJiZWMxNjcyMy1lODRlLTQ5ODQtYjdhMC1hNTJiMTExMjFjMzglMjIlMkMlMjJ1c2VySWQlMjIlM0E5NDE2MjglMkMlMjJwYXJlbnRJZCUyMiUzQTk0MTYyOCUyQyUyMnNlc3Npb25JZCUyMiUzQTE3MjU2NzgyNzkyNTYlMkMlMjJvcHRPdXQlMjIlM0FmYWxzZSUyQyUyMmxhc3RFdmVudFRpbWUlMjIlM0ExNzI1Njc4MjgwMjE0JTJDJTIybGFzdEV2ZW50SWQlMjIlM0EzNiU3RA==; JSESSIONID=818D4660E4DAFF0917475D9FD6FA0F3F"""
    headers = {"Cookie": big_seller_cookies_str}
    result = requests.get(url=url, headers=headers)
    return result.text


# 获取草稿箱列表
@app.route("/getBigSellerDraftBox", methods=["GET", "POST"])
def getBigSellerDraftBox():
    resultStr = ''
    data = request_parse(request)
    user_id = data.get("userId")

    if user_id:
        url = "https://www.bigseller.com/api/v1/product/global/shopee/draft.json?bsStatus=1&shopId=&pageNo=1&pageSize=50"
        current_cookie = next(v['cookie'] for v in g.cookie_obj if v['id'] == user_id)
        if current_cookie:
            headers = {"Cookie": current_cookie.strip()}
            request_res = requests.get(url=url, headers=headers)
            resultStr = json.dumps({
                "code": 200,
                "data": json.loads(request_res.text)
            })
        else:
            resultStr = json.dumps({
                "code": 501,
                "msg": "token不存在！！！"
            })
    else:
        resultStr = json.dumps({
            "code": 502,
            "msg": "用户id不存在"
        })
    return resultStr


if __name__ == "__main__":
    app.run("127.0.0.1", 9980, debug=False)
