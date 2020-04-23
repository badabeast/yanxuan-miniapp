from mongoengine import *


class ApiCase(Document):
    cid = StringField()
    method = StringField(required=True)
    url = StringField(required=True)
    comment = StringField()
    api_type = StringField(required=True)
    business_module = StringField()
    meta = {
        # 'collection': 'api_case_weibo',
        'collection': 'api_case',
        'strict': False
    }


class ApiRequestCase(Document):
    api_id = StringField(required=True)
    case_name = StringField()
    request_param = DictField(required=True)
    # 上游业务
    upstream = ListField()
    # 下游业务
    downstream = ListField()
    # 是否允许单独运行
    is_single_run = BooleanField()
    # 保存的值
    saved_value = DynamicField()
    key_need_to_save = DictField()
    is_sleep = StringField()
    expected_result = DictField()
    actual_result = DictField()
    # 是否是删除接口
    is_delete = BooleanField()
    # subBussinessType 新增接口才用写
    # sub_bussiness_type = StringField()
    meta = {

        #'collection': 'api_request_case_External_Interface',
        # 'collection': 'api_request_case_weibo',
        'collection': 'api_request_case',
        'strict': False,
        #'allow_inheritance': True
    }

# 抓来的数据先保存到临时表
class ApiCaseTemp(Document):
    cid = StringField()
    method = StringField(required=True)
    url = StringField(required=True)
    comment = StringField()
    api_type = StringField(required=True)
    business_module = StringField()
    meta = {
        'collection': 'api_case_temp',
        'strict': False
    }


class ApiRequestCaseTemp(Document):
    api_id = StringField(required=True)
    case_name = StringField()
    request_param = DictField(required=True)
    # 上游业务
    upstream = ListField()
    # 下游业务
    downstream = ListField()
    # 是否允许单独运行
    is_single_run = BooleanField()
    # 保存的值
    saved_value = DynamicField()
    key_need_to_save = StringField()
    is_sleep = StringField()
    expected_result = DictField()
    actual_result = DictField()
    # 是否是删除接口
    is_delete = BooleanField()
    # subBussinessType 新增接口才用写
    # sub_bussiness_type = StringField()
    meta = {

        #'collection': 'api_request_case_External_Interface',
        'collection': 'api_request_case_jxc',
        'strict': False,
        #'allow_inheritance': True
    }