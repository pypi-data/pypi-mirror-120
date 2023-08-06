import json
from functools import partial
from rainiee_rest_client.base import login, client
api_source = {
    'rainiee_data': 'https://data.rainiee.com',
    'rainiee_compute': 'https://www.rainiee.com',
    'rainiee_web': 'https://www.rainiee.com',
    'rainiee_data_test': 'http://localhost:8001',
    'rainiee_compute_test': 'http://localhost:8000',
    'rainiee_web_test': 'http://localhost:8002',
}


class RestClient(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def choice_rainiee_data(self):
        self.host = api_source['rainiee_data']
        return self

    def choice_rainiee_data_test(self):
        self.host = api_source['rainiee_data_test']
        return self

    def choice_rainiee_compute(self):
        self.host = api_source['rainiee_compute']
        return self

    def choice_rainiee_compute_test(self):
        self.host = api_source['rainiee_compute_test']
        return self

    def choice_rainiee_web(self):
        self.host = api_source['rainiee_web_test']
        return self

    def choice_rainiee_web_test(self):
        self.host = api_source['rainiee_web_test']
        return self

    def choice_other(self, host):
        self.host = host
        return self

    def login(self):
        self.token = login.LoginApi(username = self.username, password =self.password,host = self.host).login()
        return self

    def get_token(self):
        return self.token

    def __query(self, api_name, **kwargs):
        return client.DataApi(token = self.token,host = self.host).query(api_name, 'POST', req_param=kwargs)

    def __getattr__(self, name):
        return partial(self.__query, api_name=name)
