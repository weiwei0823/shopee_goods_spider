import json
import base64
import time

import requests
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from functools import wraps
from selenium.webdriver.support import expected_conditions as EC
import ddddocr
from PIL import Image
from io import BytesIO


def base64_to_img(base64_str):
    head, context = base64_str.split(",")  # 将base64_str以“,”分割为两部分
    img_data = base64.b64decode(context)  # 解码时只要内容部分

    return Image.open(BytesIO(img_data))


# 验证码登录
def handleVerifyAndLogin(driver):
    verifyCode_base64 = driver.find_element(By.XPATH, '//img[@class="cursor-pointer"]').get_attribute("src")
    # 识别验证码
    ocr = ddddocr.DdddOcr()
    verifyCode_result = ocr.classification(base64_to_img(verifyCode_base64))
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


# 获取登录cookie
def get_bigSeller_cookie():
    chrome_options = Options()
    # 设置chrome浏览器无界面模式
    # chrome_options.add_argument('--headless')
    # 启动浏览器
    temp_driver = webdriver.Chrome(options=chrome_options)

    # 访问要登录的页面
    temp_driver.get("https://www.bigseller.com/zh_CN/login.htm")

    # 获取页面源代码
    temp_driver.implicitly_wait(2)
    # 查找页面的用户名和密码输入框，并输入对应的值
    username_input = temp_driver.find_element(By.NAME, 'account')

    username_input.clear()
    username_input.send_keys("liudewei0616@gmail.com")

    password_input = temp_driver.find_element(By.NAME, 'password')
    password_input.clear()
    password_input.send_keys("ldw1987.")

    error_Result = False
    while error_Result is False:
        error_Result = handleVerifyAndLogin(temp_driver)

    # 取得登录成功后的Cookie
    cookie_dict = {}
    for cookie in temp_driver.get_cookies():
        cookie_dict[cookie['name']] = cookie['value']
    with open('big_seller.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(cookie_dict))
    # 关闭浏览器
    temp_driver.close()


def retry(max_attempts=3, delay=1, exceptions=(WebDriverException,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise
                    time.sleep(delay)

        return wrapper

    return decorator


def isElementExist(xpath_value, driver):
    flag = True
    browser = driver
    ele = browser.find_elements(by=By.XPATH, value=xpath_value)
    if len(ele) == 0:
        flag = False
        return flag
    if len(ele) == 1:
        return flag
    else:
        flag = False
        return flag


class BigSellerLogin:
    def __init__(self):
        self.timeout = 40
        self.bigSeller_info = {
            "username": "liudewei0616@gmail.com",
            "password": "Qww870823",
        }
        self.oper_status = False
        self.current_window = None
        self.auth_window_url_str = "signin/oauth/accountchooser"

    @retry(max_attempts=3, delay=2)
    def safe_find_element(self, by, value, driver, timeout=None):
        timeout = timeout or self.timeout
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    @retry(max_attempts=3, delay=2)
    def safe_click(self, element):
        element.click()

    @retry(max_attempts=2, delay=3)
    def safe_send_keys(self, element, text, is_clear=True):
        if is_clear:
            element.clear()
        element.send_keys(text)

    def open_browser(self):
        response_open_browser = requests.get(
            url=f"http://127.0.0.1:50325/api/v1/browser/start?user_id={'kwv1u5u'}"
        ).json()
        chrome_driver = response_open_browser["data"]["webdriver"]
        service = Service(executable_path=chrome_driver)
        chrome_options = Options()
        chrome_options.page_load_strategy = "eager"  # eager：等待初始HTML文档完全加载和解析，并放弃css、图像和子框架的加载。
        # chrome_options.add_argument('--headless')  # 无界面运行
        chrome_options.add_argument('--disable-gpu')  # 禁止gpu加速
        chrome_options.add_argument("no-sandbox")  # 取消沙盒模式
        chrome_options.add_argument("disable-blink-features=AutomationControlled")  # 禁用启用Blink运行时的功能
        chrome_options.add_experimental_option("debuggerAddress", response_open_browser["data"]["ws"]["selenium"])
        driver = webdriver.Chrome(service=service, options=chrome_options)
        # driver.set_window_size(400, 200)
        driver.set_page_load_timeout(self.timeout)
        driver_wait = WebDriverWait(driver, self.timeout)
        return driver

    def close_browser(self):
        response_close_browser = requests.get(
            url=f"http://127.0.0.1:50325/api/v1/browser/stop?user_id={'kwv1u5u'}",
        ).json()

    def go_bigSeller(self, driver):
        print("BigSeller登录：打开BigSeller登录页面")
        driver.get("https://www.bigseller.com/zh_CN/login.htm")
        time.sleep(4)
        return self.login_bigSeller(driver)

    def login_bigSeller(self, driver):
        login_result = {
            "result": False,
            "user_list": []
        }
        try:
            if "login.htm" in driver.current_url:
                # 输入用户名
                print("BigSeller登录：输入用户名")
                login_username_input = self.safe_find_element(By.XPATH, "//input[@name='account']",
                                                              driver)
                self.safe_send_keys(login_username_input, self.bigSeller_info["username"])
                # 输入密码
                print("BigSeller登录：输入密码")
                login_password_input = self.safe_find_element(By.XPATH, "//input[@name='password']",
                                                              driver)
                self.safe_send_keys(login_password_input, self.bigSeller_info["password"])
                is_verify_code_error = True

                # 判断验证吗并点击登录
                def check_verify_code(flag=False):
                    check_xpath = "//p[text()='图形验证码错误']"
                    time.sleep(1)
                    if isElementExist(check_xpath, driver):
                        flag = True
                    time.sleep(1)
                    if isElementExist(check_xpath, driver):
                        flag = True
                    time.sleep(1)
                    if isElementExist(check_xpath, driver):
                        flag = True
                    if "login.htm" not in driver.current_url:
                        flag = False
                    return flag

                while is_verify_code_error is True:
                    time.sleep(1)
                    print("BigSeller登录：获取验证码图片")
                    # 获取验证码图片
                    login_verify_image_div = self.safe_find_element(By.XPATH, "//img[contains(@class, 'comb-code')]",
                                                                    driver)
                    login_verify_image_base64 = login_verify_image_div.get_attribute("src")
                    print("BigSeller登录：验证码解码")
                    head, context = login_verify_image_base64.split(",")  # 将base64_str以“,”分割为两部分
                    img_data = base64.b64decode(context)  # 解码时只要内容部分
                    login_verify_image = Image.open(BytesIO(img_data))
                    ocr = ddddocr.DdddOcr()
                    verify_code = ocr.classification(login_verify_image)
                    print(f"BigSeller登录：验证码解码结果为{verify_code}")
                    # 输入验证码
                    print(f"BigSeller登录：输入验证码")
                    login_verify_input = self.safe_find_element(By.XPATH, "//input[@name='picVerificationCode']",
                                                                driver)
                    self.safe_send_keys(login_verify_input, verify_code)
                    # 点击登录按钮
                    print(f"BigSeller登录：点击登录按钮")
                    login_login_button = self.safe_find_element(By.XPATH, "//span[text()='登录']/..",
                                                                driver)
                    self.safe_click(login_login_button)
                    is_verify_code_error = check_verify_code(is_verify_code_error)

                time.sleep(2)
            # 取得登录成功后的Cookie
            cookie_dict = {}
            for cookie in driver.get_cookies():
                cookie_dict[cookie['name']] = cookie['value']
            new_token = cookie_dict["muc_token"]
            print(f"BigSeller登录：获取到新的token-{new_token}")
            user_list = self.modify_token(new_token)
            # 关闭浏览器
            login_result = {
                "result": True,
                "user_list": user_list
            }
            self.close_browser()
            return login_result
        except Exception as e:
            print("获取token报错！！！")
            driver.close()

    def modify_token(self, muc_token):
        with open('D:/开发代码/电商后台/big_seller/accountToken.json', 'r', encoding='utf-8') as f:
            content_obj = json.loads(f.read())
        # 查找并修改目标元素
        found = False
        for element in content_obj:
            if element['id'] == self.bigSeller_info["username"]:
                element['cookie']["muc_token"] = muc_token  # 修改 cookie 属性
                found = True
                break  # 假设 ID 唯一，找到后直接退出循环
        with open('D:/开发代码/电商后台/big_seller/accountToken.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(content_obj, ensure_ascii=False))
        return content_obj


if __name__ == '__main__':
    # get_bigSeller_cookie()
    bigSeller = BigSellerLogin()
    driver = bigSeller.open_browser()
    result = bigSeller.go_bigSeller(driver)
    print(result)
