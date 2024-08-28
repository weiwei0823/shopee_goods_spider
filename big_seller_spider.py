import base64
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from cnocr import CnOcr
import base64
from PIL import Image
from io import BytesIO


def base64_to_img(base64_str):
    head, context = base64_str.split(",")  # 将base64_str以“,”分割为两部分
    img_data = base64.b64decode(context)  # 解码时只要内容部分

    return Image.open(BytesIO(img_data))


def handleVerifyAndLogin(driver):
    verifyCode_base64 = driver.find_element(By.XPATH, '//img[@class="cursor-pointer"]').get_attribute("src")
    img_data = base64_to_img(verifyCode_base64)
    ocr = CnOcr(cand_alphabet="0123456789AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz")
    verifyCode_result = ocr.ocr(img_data)[0].get("text")
    print(f"Predicted Chars:{verifyCode_result}")

    verifyCode_input = driver.find_element(By.XPATH, '//input[@id="el-id-1024-7"]')
    verifyCode_input.clear()
    verifyCode_input.send_keys(verifyCode_result)

    # 查找登录按钮，点击进行登录
    login_button = driver.find_element(By.XPATH, '//button[contains(@class, "el-button--large")]')
    login_button.click()
    driver.implicitly_wait(1)
    error_pop = driver.find_element(By.XPATH, '//div[@id="message_3"]')
    return error_pop is not None


def get_bigSeller_cookie():
    # 启动浏览器
    temp_driver = webdriver.Chrome()

    # 访问要登录的页面
    temp_driver.get("https://www.bigseller.com/zh_CN/login.htm")

    # 获取页面源代码
    temp_driver.implicitly_wait(10)
    # 查找页面的用户名和密码输入框，并输入对应的值
    username_input = temp_driver.find_element(By.XPATH, '//input[@id="el-id-1024-5"]')

    username_input.clear()
    username_input.send_keys("liudewei0616@gmail.com")

    password_input = temp_driver.find_element(By.XPATH, '//input[@id="el-id-1024-6"]')
    password_input.clear()
    password_input.send_keys("ldw1987.")

    error_Result = False
    while error_Result is False:
        error_Result = handleVerifyAndLogin(temp_driver)

    # 取得登录成功后的Cookie
    cookie_dict = {}
    for cookie in temp_driver.get_cookies():
        cookie_dict[cookie['name']] = cookie['value']
    with open('ac_cert_d.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(cookie_dict))
    # 关闭浏览器
    # temp_driver.close()


if __name__ == '__main__':
    get_bigSeller_cookie()
