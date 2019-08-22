import requests
import json
import time
from zhangdama import trace_
import random
import os
from zhangdama.img_locate import ImgProcess
from zhangdama.decrypt import Encrypyed
import re

base_dir = os.path.dirname(__file__)
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
}

# 轨迹处理来自FanhuaandLuomu/geetest_break
def cal_userresponse(a, b):
    d = []
    c = b[32:]
    for e in range(len(c)):
        f = ord(str(c[e]))
        tmp = f - 87 if f > 57 else f - 48
        d.append(tmp)

    c = 36 * d[0] + d[1]
    g = int(round(a)) + c
    b = b[:32]

    i = [[], [], [], [], []]
    j = {}
    k = 0
    e = 0
    for e in range(len(b)):
        h = b[e]
        if h in j:
            pass
        else:
            j[h] = 1
            i[k].append(h)
            k += 1
            k = 0 if (k == 5) else k

    n = g
    o = 4
    p = ""
    q = [1, 2, 5, 10, 50]
    while n > 0:
        if n - q[o] >= 0:
            m = int(random.random() * len(i[o]))
            p += str(i[o][m])
            n -= q[o]
        else:
            del i[o]
            del q[o]
            o -= 1
    return p


# 由challenge+track ==> 解析得到  userresponse 和 a
def get_userresponse_a(initData, track_list):
    # 路径需要自己拟合
    challenge = initData["challenge"]
    l = track_list[-1][0]

    a = fun_f(track_list)
    arr = [12, 58, 98, 36, 43, 95, 62, 15, 12]
    s = initData["s"]
    a = fun_u(a, arr, s)
    userresponse = cal_userresponse(l, challenge)
    return userresponse, a


def fun_u(a, v1z, T1z):
    while not v1z or not T1z:
        pass
    else:
        x1z = 0
        c1z = a
        y1z = v1z[0]
        k1z = v1z[2]
        L1z = v1z[4]

        i1z = T1z[x1z : x1z + 2]
        while i1z:
            x1z += 2
            n1z = int(i1z, 16)
            M1z = chr(n1z)
            I1z = (y1z * n1z * n1z + k1z * n1z + L1z) % len(a)
            c1z = c1z[0:I1z] + M1z + c1z[I1z:]  # 插入一个值
            i1z = T1z[x1z : x1z + 2]
        return c1z


# 计算每次间隔   相当于c函数
def fun_c(a):
    g = []
    e = []
    f = 0
    for h in range(len(a) - 1):
        b = int(round(a[h + 1][0] - a[h][0]))
        c = int(round(a[h + 1][1] - a[h][1]))
        d = int(round(a[h + 1][2] - a[h][2]))
        g.append([b, c, d])

        if b == c == d == 0:
            pass
        else:
            if b == c == 0:
                f += d
            else:
                e.append([b, c, d + f])
                f = 0
    if f != 0:
        e.append([b, c, f])
    return e


def fun_e(item):  # 相当于e函数
    b = [[1, 0], [2, 0], [1, -1], [1, 1], [0, 1], [0, -1], [3, 0], [2, -1], [2, 1]]
    c = "stuvwxyz~"
    for i, t in enumerate(b):
        if t == item[:2]:
            return c[i]
    return 0


def fun_d(a):
    b = "()*,-./0123456789:?@ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqr"
    c = len(b)
    d = ""
    e = abs(a)
    f = int(e / c)
    if f >= c:
        f = c - 1
    if f > 0:
        d = b[f]
    e %= c
    g = ""
    if a < 0:
        g += "!"
    if d:
        g += "$"
    return g + d + b[e]


def fun_f(track_list):
    skip_list = fun_c(track_list)
    g, h, i = [], [], []
    for j in range(len(skip_list)):
        b = fun_e(skip_list[j])
        if b:
            h.append(b)
        else:
            g.append(fun_d(skip_list[j][0]))
            h.append(fun_d(skip_list[j][1]))
        i.append(fun_d(skip_list[j][2]))
    return "".join(g) + "!!" + "".join(h) + "!!" + "".join(i)


def get_new_challenge(session, gt, challenge):
    url = "https://api.geetest.com/get.php"
    params = {
        "gt": gt,
        "challenge": challenge,
        "offline": "false",
        "new_captcha": "true",
        "product": "bind",
        "protocol": "https://",
        "pencil": "/static/js/pencil.1.0.3.js",
        "type": "slide",
        "path": "/static/js/geetest.6.0.9.js",
        "maze": "/static/js/maze.1.0.1.js",
        "beeline": "/static/js/beeline.1.0.1.js",
        "voice": "/static/js/voice.1.2.0.js",
        "callback": "geetest_" + str(int(time.time() * 1000)),
    }
    response = session.get(url, params=params, headers=headers).text
    res = re.search(r"({.*})", response[:-1]).group()
    res = json.loads(res)
    return res


def crack(gt, challenge, referer, session):
    response = get_new_challenge(session, gt, challenge)
    challenge = response["challenge"]

    # 下载图片
    fullbg = str(time.time()) + str(random.random())
    bg = str(time.time()) + str(random.random())
    open(base_dir + "/Image/" + fullbg + ".jpg", "wb").write(
        session.get(
            "https://static.geetest.com/" + response["fullbg"], headers=headers
        ).content
    )
    open(base_dir + "/Image/" + bg + ".jpg", "wb").write(
        session.get("https://static.geetest.com/" + response["bg"]).content
    )

    # 图片处理
    # 代码改自 OSinoooO/bilibili_geetest
    img_process = ImgProcess()
    img1 = img_process.get_merge_image(base_dir + "/Image/" + fullbg + ".jpg")
    img2 = img_process.get_merge_image(base_dir + "/Image/" + bg + ".jpg")
    os.remove(base_dir + "/Image/" + fullbg + ".jpg")
    os.remove(base_dir + "/Image/" + bg + ".jpg")
    distance = int(img_process.get_gap(img1, img2) - 7)

    track = trace_.choice_track(distance)
    userresponse, aa = get_userresponse_a(response, track)
    passtime = track[-1][-1]
    time.sleep(1)
    ep = Encrypyed()
    params = ep.encrypted_request(response, userresponse, passtime, aa)
    response = session.get(
        "https://api.geetest.com/ajax.php", params=params, headers=headers
    )
    print("geetest返回结果:{}".format(response.text))
    try:
        return response.json(), challenge
    except:
        if "geetest" in response.text:
            text = re.sub("geetest_\d*\(", "", response.text)
            return json.loads(text[:-1]), challenge
        else:
            return json.loads(response.text[1:-1]), challenge
