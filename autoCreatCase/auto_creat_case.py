# coding:utf-8
import json
import os
from utils.mongoconnect import MongoConnect
from orm.ormdb import ApiCase, ApiRequestCase
from utils.filereader import InIReader


USING_ENV = "UAT"

# 连接mongodb, 使用配置文件
dealut_connection = MongoConnect()

# Config
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
configfile = os.path.join(current_dir, "conf", "conf.ini")
config = InIReader(configfile).config

# har_path = '/Users/hushunxuan/workspace/mypython/blog/blogapp/ptfweb.xbongbong.com.har'
har_path = r'C:\Users\56835\Desktop\pro_weibo.har'


def get_repeat_attr(response_json):
    if isinstance(response_json, str):
        response_json = json.loads(response_json)
    else:
        response_json = response_json
    attr_list = []
    explainList = response_json['result']['explainList']
    for explain in explainList:
        if explain.get('noRepeat') == 1:
            attr_list.append(
                {
                    'attr': explain.get('attr'),
                    'fieldType': explain.get('fieldType'),
                    'attrName': explain.get('attrName'),
                    'attrType': explain.get('attrType'),
                }
            )
    return attr_list


with open(har_path, 'r',encoding="utf-8") as xbb_har:
    f = xbb_har.read()

    bb = json.loads(f, encoding='utf-8')
    i = 0
    n = 0
    y = 0
for xbb_request in bb['log']['entries']:
    if not xbb_request['request']['url'].endswith('.js') \
            and (xbb_request['request']['url'].startswith('https://ptfweb.xbongbong.com/')
                 or xbb_request['request']['url'].startswith('https://testdingtalkapi3.xbongbong.com/'))\
            and xbb_request['request']['method'] == 'POST':

        if xbb_request['request']['url'].startswith('https://ptfweb.xbongbong.com/'):
            cid = xbb_request['request']['url'][29:].replace('/', '_')
            api_type = 'web'
            url = '/' + xbb_request['request']['url'][29:]

        elif xbb_request['request']['url'].startswith('https://testdingtalkapi3.xbongbong.com/'):
            cid = xbb_request['request']['url'][39:].replace('/', '_')
            api_type = 'app'
            url = '/' + xbb_request['request']['url'][39:]

        method = xbb_request['request']['method']
        comment = ''
        businessType = str(json.loads(xbb_request['request']['postData']['text']).get('businessType'))
        business_module = businessType

        api_id = cid
        if businessType:
            case_name = 'autoCreate_' + api_id + '_businessType_' + businessType
        else:
            case_name = 'autoCreate_' + api_id
        request_param = xbb_request['request']['postData']['text']

        key_need_to_save = {}
        is_sleep = 1
        expected_result = {'code': 1, 'msg': '操作成功'}
        actual_result = xbb_request['response']['content']['text']
        if not (json.loads(actual_result)['code'] == 1):
            print(1)
            continue

        case_data = ApiCase.objects(cid=cid.lower()).first()
        request_case_data = ApiRequestCase.objects(case_name=case_name).first()

        request_json = json.loads(request_param)

        if not case_data:
            ApiCase(cid=cid.lower(),
                         comment=comment,
                         url=url,
                         method=method,
                         business_module=business_module,
                         api_type=api_type).save()

        case_data = ApiCase.objects(cid=cid.lower()).first()
        # 保存之前没有的
        if case_data and (not request_case_data):
            y = y+1
            try:
                ApiRequestCase(api_id=api_id.lower(),
                                    case_name=case_name,
                                    request_param=request_json,
                                    upstream=[],
                                    downstream=[],
                                    is_single_run=True,
                                    saved_value={},
                                    key_need_to_save=key_need_to_save,
                                    is_sleep='1',
                                    expected_result=expected_result,
                                    actual_result=json.loads(actual_result)
                                    ).save()
            except Exception as e:
                print(e)

for xbb_request in bb['log']['entries']:
    if not xbb_request['request']['url'].endswith('.js') \
            and (xbb_request['request']['url'].startswith('https://ptfweb.xbongbong.com/')
                 or xbb_request['request']['url'].startswith('https://testdingtalkapi3.xbongbong.com/')) \
            and xbb_request['request']['method'] == 'POST':

        if xbb_request['request']['url'].startswith('https://ptfweb.xbongbong.com/'):
            cid = xbb_request['request']['url'][29:].replace('/', '_')
            api_type = 'web'
            url = '/' + xbb_request['request']['url'][29:]

        elif xbb_request['request']['url'].startswith('https://testdingtalkapi3.xbongbong.com/'):
            cid = xbb_request['request']['url'][39:].replace('/', '_')
            api_type = 'app'
            url = '/' + xbb_request['request']['url'][39:]

        method = xbb_request['request']['method']
        comment = ''
        businessType = str(json.loads(xbb_request['request']['postData']['text']).get('businessType'))
        business_module = businessType

        api_id = cid
        if businessType:
            case_name = 'autoCreate_' + api_id + '_businessType_' + businessType
        else:
            case_name = 'autoCreate_' + api_id
        request_param = xbb_request['request']['postData']['text']
        key_need_to_save = ''
        is_sleep = 1
        expected_result = {'code': 1, 'msg': '操作成功'}
        actual_result = xbb_request['response']['content']['text']

        if not json.loads(actual_result)['code'] == 1:
            continue

        case_data = ApiCase.objects(cid=cid.lower()).first()
        request_case_data = ApiRequestCase.objects(case_name=case_name).first()

        request_json = json.loads(request_param)
        # if actual_result:
        #     actual_json = json.loads(actual_result)
            # if case_name == 'autoCreate_pro_v1_mobile_getBusinessStageArray_businessType_108':
            #     if actual_json.get('result'):
            #         if isinstance(actual_json.get('result'), dict):
            #             if actual_json.get('result').get('formDataId') == '195275':
            #                 print(request_json)
            #                 print(case_name)
        if api_id == 'pro_v1_mobile_form_data_add':
            case_name1 = 'autoCreate_pro_v1_mobile_form_data_add_get_businessType_' + businessType
            key_need_to_save = {
                'dataId': 'actual_result.result.formDataId'
            }
            add_get_case = ApiRequestCase.objects(case_name=case_name1).first()
            if add_get_case:
                actual_result1 = add_get_case.actual_result
                # print(actual_result1)
                attr_list = get_repeat_attr(actual_result1)
                for attr in attr_list:
                    attr1 = attr['attr']
                    request_json['dataList'][attr1] = '${faker@people_name}'

        if businessType and request_json.get('dataId'):
            request_json['dataId'] = '${autoCreate_pro_v1_mobile_form_data_add_businessType_' + businessType + '@dataId}'

        # 保存之前没有的
        if request_case_data:
            request_case_data.update(request_param=request_json,
                                     key_need_to_save=key_need_to_save)

if __name__ == '__main__':
    pass
