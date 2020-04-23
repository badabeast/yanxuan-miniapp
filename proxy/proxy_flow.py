import sys,pprint,pathlib,os
sys.path.append(os.getcwd())
# pprint.pprint(sys.path)
from mitmproxy import http
from mongoengine.errors import ValidationError
from orm.ormdb import ApiRequestCaseTemp,ApiCaseTemp,ApiRequestCase
from utils.log import Log
"""
Script for mitmdump
"""
from utils.mongoconnect import MongoConnect
import json
import time

logger = Log()
default_connection = MongoConnect()

global i 
i = 0

def request(flow: http.HTTPFlow):
    # TODO:后续可以使用配置过滤器
    hosts = ["ptfweb.xbongbong.com","testdingtalkapi3.xbongbong.com"]
    if (flow.request.host not in hosts) or flow.request.method != "POST" or (flow.request.path.endswith('js') or  flow.request.path.endswith('css')):
        return
    api_type = 'web' if flow.request.host == "ptfweb.xbongbong.com" else "app"
    try:
        api_id = flow.request.path[1:].replace('/', '_')
        if not ApiCaseTemp.objects(cid=api_id.lower()).first():
            logger.debug('unknow.url:' + flow.request.path)
            # 把没有的接口用例加进去
            ApiCaseTemp(
                cid = api_id,
                method = 'POST',
                url = flow.request.path,
                comment = '未处理的URL',
                api_type = 'web',
                business_module = ''
            ).save()
    except Exception as e:
        logger.error("保存ApiCaseTemp临时库出错:" + str(e))

def responseheaders(flow):
    """
    Enables streaming for all responses.
    This is equivalent to passing `--set stream_large_bodies=1` to mitmproxy.
    """
    flow.response.stream = False

def response(flow):
    hosts = ["ptfweb.xbongbong.com","testdingtalkapi3.xbongbong.com"]
    if (flow.request.host not in hosts) or flow.request.method != "POST" or (flow.request.path.endswith('js') or  flow.request.path.endswith('css')):
        return
    api_id = flow.request.path[1:].replace('/', '_')
    request_param = json.loads(flow.request.text)
    expected_result = {'code': 1, 'msg': '操作成功'}
    if 'dataId' in request_param:
        if request_param['dataId'] is not None:    
            sbt = request_param['subBusinessType'] if 'subBusinessType' in request_param else request_param['businessType']
            realted_add_request = ApiRequestCase.objects(api_id="pro_v1_form_data_add",request_param__subBusinessType = int(sbt)).first()
            logger.debug(str(realted_add_request.case_name))
            request_param['dataId'] = "${" + str(realted_add_request.case_name) + "@dataId}"
    try:
        global i 
        i += 1
        ApiRequestCaseTemp(api_id=api_id,
                        case_name= "代理抓取_" + str(i),
                        request_param=request_param,
                        upstream=[],
                        downstream=[],
                        is_single_run=True,
                        saved_value='',
                        key_need_to_save='',
                        is_sleep='1',
                        expected_result=expected_result,
                        actual_result=json.loads(flow.response.text) # actual_result需要拦截response请求去处理
                        ).save()
    except ValidationError as e:
        ApiRequestCaseTemp(api_id=api_id,
                case_name= "代理抓取_" + str(i),
                request_param=request_param,
                upstream=[],
                downstream=[],
                is_single_run=True,
                saved_value='',
                key_need_to_save='',
                is_sleep='1',
                expected_result=expected_result
                ).save()
        logger.info("报错了:"+ str(e) +",没能保存实际结果。")
    except Exception as e:
        logger.error("保存临时库出错:" + str(e))
