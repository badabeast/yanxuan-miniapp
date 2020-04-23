# -*- coding: UTF-8 -*-
import requests
import json, hashlib
import hmac
from utils.log import Log

logger = Log()


class XbbRequest:
    # 共享变量
    app_session = requests.session()
    # Web后台session初始化
    web_session = requests.session()

    def __init__(self, platform: str, url: str, params: json, token: str):
        self.header = {
            'Content-Type': 'application/json;charset=UTF-8',
        }
        self.platform = platform
        self.url = url
        self.params = params
        self.strparams = self.json2str(params)
        self.token = token

    def post(self):
        logger.debug("请求URL:" + self.url)
        logger.debug("请求参数:" + str(self.params))

        sign = self.__gen_sign_code(self.params, self.token)
        self.header["sign"] = sign
        if self.platform == "web":
            res = self.web_session.post(headers=self.header, data=self.strparams, url=self.url)
        else:
            res = self.app_session.post(headers=self.header, data=self.strparams, url=self.url)
        logger.debug("返回结果:" + str(res.text))
        # print(res.text)
        return res

    def __gen_sign_code(self, request_parameters, xbb_access_token):
        """
        生成请求发送时的sign_code值
        Web&App共用一个xbb_access_token
        """

        if self.platform == 'api':
            parameters = (json.dumps(request_parameters, separators=(',', ':'),
                                     ensure_ascii=False) + xbb_access_token).encode("utf-8")
            # parameters = (self.json2str(request_parameters) + xbb_access_token).encode("utf-8")
        else:
            parameters = (self.json2str(request_parameters) + xbb_access_token).encode("utf-8")
        return hashlib.sha256(parameters).hexdigest()

    @staticmethod
    def json2str(data):
        return json.dumps(data, separators=(',', ':'))


if __name__ == "__main__":
    pass
    host = 'http://ptapi.xbongbong.com'
    token = 'test_token_ding4a3aebc0873df49335c2f4657eb6378f'

    # host = 'http://192.168.10.64:2009'
    # token = '1b5f9765a8e55b18af0cf35fc04b2176'

    # url = '/pro/v1/api/user/list'
    url = '/pro/v1/api/form/list'

    corp_id = 'ding4a3aebc0873df49335c2f4657eb6378f'
    user_id = '212708396132942386'
    request_json = {
        "name": "模板",
        "saasMark": 1,
        "businessType": 201,
        "corpid": "ding4a3aebc0873df49335c2f4657eb6378f",
        "userId": "212708396132942386"
    }
    xbbrequest = XbbRequest('api', host + url, request_json, token)
    res = xbbrequest.post()
    print(res.text)
