import json

from selenium import webdriver
from selenium.webdriver.common.by import By


def get_cookie():
    # 启动浏览器
    temp_driver = webdriver.Chrome()

    # 访问要登录的页面
    temp_driver.get("https://shopee.com.my/buyer/login")

    # 获取页面源代码
    temp_driver.implicitly_wait(10)
    # 选择语言，如果弹出则点击
    modal_div = temp_driver.find_element(By.XPATH, '//div[@id="modal"]')
    if modal_div is not None:
        language_button = modal_div.find_element(By.XPATH, '//button[contains(text(), "简体中文")]')
        language_button.click()
        temp_driver.implicitly_wait(10)
    # 查找页面的用户名和密码输入框，并输入对应的值
    username_input = temp_driver.find_element(By.XPATH, '//input[@name="loginKey"]')

    username_input.clear()
    username_input.send_keys("liudewei0616")

    password_input = temp_driver.find_element(By.XPATH, '//input[@name="password"]')
    password_input.clear()
    password_input.send_keys("Ldw19870616")

    # 查找登录按钮，点击进行登录
    login_button = temp_driver.find_element(By.XPATH, '//button[text()="登入"]')
    login_button.click()
    # 取得登录成功后的Cookie
    cookie_dict = {}
    for cookie in temp_driver.get_cookies():
        cookie_dict[cookie['name']] = cookie['value']
    with open('ac_cert_d.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(cookie_dict))
    # 关闭浏览器
    temp_driver.close()


# get_cookie()

if __name__ == '__main__':
    get_cookie()
