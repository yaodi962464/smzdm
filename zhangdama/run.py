from zhangdama import geetest


def gee(session, geetest_code_url):
    while True:
        # total = total + 1
        geeData = session.get(
            geetest_code_url,
            headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"}
        ).json()
        # print(geeData)
        referer = "https://zhiyou.smzdm.com/user/login/window/"
        ans, challenge = geetest.crack(geeData["gt"], geeData["challenge"], referer, session)

        try:
            r = ans['validate']
            return ans['validate'], geeData, challenge
        except KeyError:
            pass

