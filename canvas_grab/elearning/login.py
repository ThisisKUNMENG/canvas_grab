from sys import exit as sys_exit
import re
import requests
from requests import adapters
import ssl

import urllib3


class CustomHttpAdapter(requests.adapters.HTTPAdapter):
    """Transport adapter" that allows us to use custom ssl_context."""

    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context)


def get_legacy_session():
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
    session = requests.session()
    session.mount('https://', CustomHttpAdapter(ctx))
    return session


class Fudan:
    """
    建立与复旦服务器的会话，执行登录/登出操作
    """
    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
         "(KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"

    # 初始化会话
    def __init__(self,
                 uid, psw,
                 url_login='https://uis.fudan.edu.cn/authserver/login',
                 url_code="https://zlapp.fudan.edu.cn/backend/default/code"):
        """
        初始化一个session，及登录信息
        :param uid: 学号
        :param psw: 密码
        :param url_login: 登录页，默认服务为空
        """
        self.session = get_legacy_session()
        self.session.keep_alive = True
        self.session.headers['User-Agent'] = self.UA
        self.url_login = url_login
        self.url_code = url_code

        self.uid = uid
        self.psw = psw

    def _page_init(self):
        """
        检查是否能打开登录页面
        :return: 登录页page source
        """
        print("◉Initiating——", end='')
        page_login = self.session.get(self.url_login)

        print("return status code",
              page_login.status_code)

        if page_login.status_code == 200:
            print("◉Initiated——", end="")
            return page_login.text
        else:
            print("◉Fail to open Login Page, Check your Internet connection\n")
            self.fail(page_login.status_code)

    def login(self, is_elearning=False):
        """
        执行登录
        """
        page_login = self._page_init()

        print("getting tokens")
        data = {
            "username": self.uid,
            "password": self.psw,
        }

        # 获取登录页上的令牌
        result = re.findall(
            '<input type="hidden" name="([a-zA-Z0-9\-_]+)" value="([a-zA-Z0-9\-_]+)"/?>', page_login)
        # print(result)
        # result 是一个列表，列表中的每一项是包含 name 和 value 的 tuple，例如
        # [('lt', 'LT-6711210-Ia3WttcMvLBWNBygRNHdNzHzB49jlQ1602983174755-7xmC-cas'),
        # ('dllt', 'userNamePasswordLogin'), ('execution', 'e1s1'), ('_eventId', 'submit'), ('rmShown', '1')]
        data.update(result)

        headers = {
            "Host": "uis.fudan.edu.cn",
            "Origin": "https://uis.fudan.edu.cn",
            "Referer": self.url_login,
            "User-Agent": self.UA
        }

        print("◉Login ing——", end="")
        if is_elearning:
            post = self.session.post(
                self.url_login,
                data=data,
                headers=headers,
                allow_redirects=False)
            cas_header = {
                "Referer": "https://uis.fudan.edu.cn/",
                "User-Agent": self.UA,
            }
            cas = self.session.get(
                post.headers.get('Location'),
                headers=cas_header,
                allow_redirects=False)
            if cas.status_code == 302:
                print("\n***********************"
                      "\n◉成功登录elearning"
                      "\n***********************\n")
        else:
            post = self.session.post(
                self.url_login,
                data=data,
                headers=headers,
                allow_redirects=False)

        print("return status code", post.status_code)

        if post.status_code == 302:
            print("\n***********************"
                  "\n◉登录成功"
                  "\n***********************\n")
        else:
            print("◉登录失败，请检查账号信息")
            self.close()

    def logout(self):
        """
        执行登出
        """
        exit_url = 'https://uis.fudan.edu.cn/authserver/logout?service=/authserver/login'
        expire = self.session.get(exit_url).headers.get('Set-Cookie')
        # print(expire)

        if '01-Jan-1970' in expire:
            print("◉登出完毕")
        else:
            print("◉登出异常")

    def close(self):
        """
        执行登出并关闭会话
        """

        self.logout()
        self.session.close()
        print("◉关闭会话")
        print("************************")

    def fail(self, exit_code):
        sys_exit(exit_code)
