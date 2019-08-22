# -*- coding: utf-8 -*-
"""
Time    : 2019-08-20 16:58
Author  : yuyuyu
Object  : 
"""
# python 内置库
import json
import re
import time
import base64

# python 第三方库
import requests

# python 项目库
from zhangdama import run
from zhangdama.rea_handle import crack_pwd


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit"
    "/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
    "Referer": "https://zhiyou.smzdm.com",
    "Accept": "text/javascript, application/javascript, "
    "application/ecmascript, application/x-ecmascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
}
session = requests.session()


def get_geetest_challenge(username, password):
    geetest_code_url = "https://zhiyou.smzdm.com/user/getgeetest/captcha_init?rand=64"
    login_url = "https://zhiyou.smzdm.com/user/login/ajax_normal_check"
    checkin_url = "https://zhiyou.smzdm.com/user/checkin/jsonp_checkin?callback= &_={}".format(
        time.time() * 1000
    )
    s = run.gee(session, geetest_code_url)
    validate, geeData, new_challenge = s
    # 获取公钥
    pub_key_url = "https://zhiyou.smzdm.com/user/login/pre"
    pub_key = (
        session.get(pub_key_url, headers=headers).json().get("data").get("pub_key")
    )
    # 获取密码
    password = crack_pwd(password, pub_key)

    data = {
        "username": base64.b64encode(username.encode()).decode(),
        "password": password,
        "rememberme": 1,
        "captcha": "",
        "redirect_to": "",
        "geetest_challenge": new_challenge,
        "geetest_validate": validate,
        "geetest_seccode": "{}|jordan".format(validate),
    }

    login_res = session.post(login_url, data=data, headers=headers)
    print("登陆结果:{}".format(login_res.json()))
    if login_res.json().get("error_code") != 0:
        print("登陆失败")
        return
    time.sleep(1)

    response = session.get(checkin_url, headers=headers)

    check_res = response.text.replace("callback(", "")[:-1]
    check_res_json = json.loads(check_res)
    res = re.findall(r".*?>(.*?)<", str(check_res_json["data"]))
    print("".join(res))


if __name__ == "__main__":
    get_geetest_challenge(username="yaorUserName", password="yourPassword")
