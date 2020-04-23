# encoding = utf-8
# Author：晴空


import requests
import re
import hashlib
import os
import json
import time
from assertpy import soft_assertions
from assertpy import assert_that
from utils.mongoconnect import MongoConnect
from orm.ormdb import ApiCase,ApiRequestCase
from utils.filereader import InIReader
from Xrequest.request import XbbRequest
from utils.constant import Constant
from utils.log import Log



USING_ENV = "UAT"

logger = Log()
# 连接mongodb, 使用配置文件
dealut_connection = MongoConnect()

# Config
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
configfile = os.path.join(current_dir, "conf", "conf.ini")
config = InIReader(configfile).config

# 查找测试用例中需替换内容时所用的正则表达式 
# 正确的格式如: ${time@current_minute} ${faker@phone} ${正常新增客户数据@dataId}
#修改前
# re_str = '[()a-zA-Z_]{1,}@[0-9a-zA-Z_]{1,}'
#修改后
re_str = '\'\$\{[()a-zA-Z_\u4e00-\u9fa5]{1,}@[0-9a-zA-Z_]{1,}\}\''


# 预编译正则表达式
pattern = re.compile(re_str)


# 断言实际结果包含预期结果
def assert_result(case_name):
    case_data = get_request_case_data(case_name)
    actual_result = case_data.actual_result
    expected_result = case_data.expected_result
    # 判断是否需要断言
    if len(expected_result) == 0:
        pass
    else:
        with soft_assertions():

            # assert_that(dict(actual_result)).contains_entry(expected_result)
            assert_that(expected_result).is_subset_of(actual_result)


# 获得接口用例信息
def get_request_case_data(case_name):
    case_data = ApiRequestCase.objects(case_name=case_name).first()
    return case_data


# 先执行依赖接口 获得接口的上游和下游业务
def get_refer_business_interface(case_name):
    case_data = ApiRequestCase.objects(case_name=case_name).first()

    return find_refer_no_saved_value([case_name]) + case_data.upstream + [case_name] + case_data.downstream


# 获取接口URL类型
def get_api_type(api_id):
    api_case_data = ApiCase.objects(cid = api_id).first()
    return api_case_data.api_type


# 获得接口URL地址
def get_api_url(api_id):
    api_case_data = ApiCase.objects(cid = api_id).first()
    if get_api_type(api_id) == "web":
        return config.get(USING_ENV, "weburl")+api_case_data.url
    elif get_api_type(api_id) == "api":
        return config.get(USING_ENV, "apiurl") + api_case_data.url
    else:
        return config.get(USING_ENV,"appurl")+api_case_data.url


# 接口用例参数依赖处理
def replace_relate_param(case_data, *args):
    # 用例中的请求参数
    case_param = case_data.request_param

    # 正则查找匹配项
    matchers = pattern.findall(str(case_param))
    # 判断请求参数中是否有依赖其他用例的数据
    if 0 == len(matchers):
        pass
    else:
        for matcher in matchers:
            # 被依赖的用例名称
            # relate_case_name = matcher.split('@')[0][3:]
            # 修改前
            relate_case_name = matcher.split('@')[0][2:]
            # be_related_data = matcher.split('@')[1][:-2]
            # 修改前
            be_related_data = matcher.split('@')[1][:-1]
            logger.info("被依赖的用例名称:"+relate_case_name)
            # 替换请求参数中使用的时间
            if relate_case_name == 'time' or relate_case_name == 'faker':
                case_param = str(case_param).replace(str(matcher), str(eval('Constant.'+be_related_data)()))
                logger.info('正在替换参数%s为%s' % (str(matcher), str(eval('Constant.'+be_related_data)())))
            # 用实际值替换依赖其他用例的数据
            else:
                # 多个接口的业务用例，用测试步骤中的数据替换参数   
                relate_case_data = ApiRequestCase.objects(case_name=relate_case_name).first()
                logger.info('正在替换参数%s为%s' % (str(matcher), str(relate_case_data.saved_value[be_related_data])))
                case_param = str(case_param).replace(str(matcher), str(relate_case_data.saved_value[be_related_data]))
                #  TODO 对于复杂替换字段用json转化未字符串
                # case_object=HandleJson(relate_case_data)
                # case_object.find_value_path(matcher)
                # 如果接口是删除接口，case_param替换过后，再把这个relate_case的value置空，相当于消费掉
                if case_data.is_delete == True:
                    relate_case_data.update(saved_value = None)
    # check
    case_param = eval(str(case_param))

    for k,v in case_param.items():
        try:
            if type(v) == str:
                case_param[k] = eval(v)
        except Exception as e:
            pass
    # 不要改变变量类型  动态语言真的坑
    return case_param


# 保存被依赖的值
def update_relate_key_value(document, value_need_to_save):
    document.update(saved_value=value_need_to_save)


# 保存实际结果
def update_actual_result(document, actual_result):
    from mongoengine.errors import ValidationError
    try:
        document.update(actual_result=json.loads(actual_result.text))
    except ValidationError as ve:
        logger.error("保存实际结果出错，跳过保存。")

# 发送Web，App后台请求
def exec_xbb_request(case_name, platform):
    case_data = get_request_case_data(case_name)
    request_content = replace_relate_param(case_data)
    api_url = get_api_url(case_data.api_id)
    token = config.get(USING_ENV, "token")

    xbb_request = XbbRequest(platform,api_url,request_content,token)
    actual_result = xbb_request.post()
    update_actual_result(case_data, actual_result)
    key_need_to_save = case_data.key_need_to_save
    try:
        if  key_need_to_save is None or len(key_need_to_save) == 0:
            pass
        else:
            saved_value = {}
            for k,v in key_need_to_save.items():
                if v.split('.')[0] == 'request_param':
                    saved_value[k] = parse_jsonpath({'request_param':request_content},v)
                else:
                    saved_value[k] = parse_jsonpath({'actual_result':json.loads(actual_result.text)},v)
            update_relate_key_value(case_data, saved_value)
    except Exception as e:
        logger.error(e)
        logger.error("保存失败,请求返回结果为:"+ actual_result.text)

    # 保存接口调用需要注意时间间隔是7s
    is_sleep = case_data.is_sleep
    if str(1) == is_sleep:
        time.sleep(3)
    else:
        pass

# 解析json结果
def parse_jsonpath(data:dict,path:str):
    value = data
    pathlist = path.split('.')
    for p in pathlist:
        #TODO:支持取出列表中的几个
        if p.endswith(']'):
            left_index = p.index('[')
            value = value[p[:0-len(p)+left_index]]
            value = eval('value'+p[0-len(p)+left_index:])
            continue
        elif isinstance(value,dict) and not p.endswith(']'):
            value = value[p]
            continue
        elif isinstance(value,list):
            o = value
            value = []
            for q in o:
                value.append(q[p])
        else:
            pass
    return value

refer_list = []
# 获取没有的保存值的相关用例，返回case依赖case的列表，变相排序
def find_refer_no_saved_value(case_names):
    tl = []
    for case_name in case_names:
        case_data = get_request_case_data(case_name)
        case_param = case_data.request_param
        matchers = pattern.findall(str(case_param))
        for matcher in matchers:
            # relate_case_name = matcher.split('@')[0][3:]
            # 下面的是原始代码
            relate_case_name = matcher.split('@')[0][2:]
            if relate_case_name in ['faker','time'] or relate_case_name in case_data.upstream:
                pass
            else:
                relate_case_data = ApiRequestCase.objects(case_name=relate_case_name).first()
                if  len(relate_case_data.saved_value) == 0 or relate_case_data.saved_value is None:
                    tl.append(relate_case_data.case_name)
    global refer_list
    refer_list = refer_list + tl
    if len(tl)> 0:
        find_refer_no_saved_value(tl)
    reverse_list = refer_list[::-1]
    t = list(set(reverse_list))
    t.sort(key=reverse_list.index)
    return t

# 封装所有用例执行
def exe_case(case_name):
    case_data = get_request_case_data(case_name)
    api_type = get_api_type(case_data.api_id)
    try:
        refer_business_interface = get_refer_business_interface(case_name)
        logger.info("该业务%s执行相关的业务:%s" % (case_name,str(refer_business_interface)))
        # 执行业务
        for business in refer_business_interface:
            logger.info("正在执行的业务:" + business)
            exec_xbb_request(business, api_type)
    except Exception as e:
        logger.error(e)
    finally:
        global refer_list
        refer_list = []