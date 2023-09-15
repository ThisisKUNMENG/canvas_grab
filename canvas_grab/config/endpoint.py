from ..configurable import Configurable, Interactable
from canvasapi import Canvas
from ..elearning import Fudan
import questionary


class Endpoint(Configurable, Interactable):
    """Endpoint stores Canvas LMS endpoint and API key.
    """

    def __init__(self):
        self.endpoint = 'https://elearning.fudan.edu.cn'
        self.api_key = ''
        self.account = ''
        self.password = ''
        self.session = None

    def to_config(self):
        return {
            'endpoint': self.endpoint,
            'api_key': self.api_key,
            'account': self.account,
            'password': self.password,
            'session': self.session
        }

    def from_config(self, config):
        self.endpoint = config['endpoint']
        self.api_key = config['api_key']
        self.account = config['account']
        self.password = config['password']

    def interact(self):
        self.endpoint = questionary.text(
            'Canvas API endpoint', default=self.endpoint).unsafe_ask()
        self.api_key = questionary.text(
            'API Key', default=self.api_key,
            instruction="Please visit profile page of Canvas LMS to generate an access token").unsafe_ask()
        self.account = questionary.text(
            'Account', default=self.account).unsafe_ask()
        self.password = questionary.password(
            'Password', default=self.password).unsafe_ask()

    def login(self):
        if self.api_key == '':
            elearning = Fudan(uid=self.account, psw=self.password,
                             url_login='https://uis.fudan.edu.cn/authserver/login'
                                       '?service=https%3A%2F%2Felearning.fudan.edu.cn%2Flogin%2Fcas%2F3')
            elearning.login(is_elearning=True)
            self.session = elearning.session
        return Canvas(self.endpoint, self.api_key, self.session)
