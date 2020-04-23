import os,hashlib,json
from configparser import ConfigParser

# 5dcadf8b2543219809b26d23d1b458ddf88a3c669fac5e504e1dff5545ffc81f
def create_sign_code(request_parameters, xbb_access_token):
    """
        生成请求发送时的sign_code值
        Web&App共用一个xbb_access_token
    """
    parameters = (json.dumps(request_parameters,separators=(',',':'))  + xbb_access_token).encode('utf-8')
    print(json.dumps(request_parameters))
    return hashlib.sha256(parameters).hexdigest()

token = "75ced70105bc2af55af99d5a3f90e3170c587161bd3495d7b3b763ab92c49a6a"
json2 = "{\"corpid\":\"ding4a3aebc0873df49335c2f4657eb6378f\",\"userId\":\"06324232141219021\",\"platform\":\"web\",\"sortMap\":{},\"formId\":1071,\"saasMark\":1,\"businessType\":100,\"subBusinessType\":101,\"listGroupId\":0,\"defaultGroup\":1,\"commonFilter\":{},\"del\":0,\"page\":1,\"pageSize\":20,\"conditions\":[],\"statusFilter\":2,\"appId\":239}"
json1 = {"corpid":"ding4a3aebc0873df49335c2f4657eb6378f","userId":"06324232141219021","platform":"web","sortMap":{},"formId":1071,"saasMark":1,"businessType":100,"subBusinessType":101,"listGroupId":0,"defaultGroup":1,"commonFilter":{},"del":0,"page":1,"pageSize":20,"conditions":[],"statusFilter":2,"appId":239}

def process_headers(request_parameters, token):
    parameters = str(str(request_parameters) + str(token)).encode('utf-8')
    sign_code = hashlib.sha256(parameters).hexdigest()
    return sign_code

def test_gen_sign():
    assert create_sign_code(json1,token) == process_headers(json2,token)