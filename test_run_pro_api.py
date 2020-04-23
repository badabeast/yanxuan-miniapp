# -*- encoding = utf-8 -*-
import pytest, os
from utils import basic
from utils.mongoconnect import MongoConnect
from orm.ormdb import ApiRequestCase

# 使用的测试环境 UAT测试环境 PROD生产环境
USING_ENV = "UAT"
# 根据ini生成默认的MongoDB连接
default_connection = MongoConnect()


# 获得所有用例名称,以数组形式存储
# 默认执行所有的API接口用例,平台化之后可传入测试计划名称作为参数来执行指定的用例集
def get_all_case_name(case_name=None):
    name_list = []
    # 判断是否传入测试计划名称
    if case_name is None:
        all_request_cases = ApiRequestCase.objects().all()
        print(all_request_cases)
    else:
        # TODO: 传入测试计划名称
        # all_case_name_data = mongodb_conn["api_test_plan"].find({}, {"_id": 0, "case_name": "1"})
        return
    # 遍历查询需要执行的用例信息,存储用例名称
    for request_case in all_request_cases:
        # if request_case.is_single_run is None or request_case.is_single_run:
        if request_case.is_single_run is None or request_case.is_single_run or not request_case.is_delete: #测试不运行删除接口
            name_list.append(request_case.case_name)
    return name_list

# 还原作案现场
restore_site_crm_case = ['批量删除退货退款','批量删除合同订单','批量删除销售机会','批量删除联系人','批量删除全部客户']


# 定义pytest参数化使用的参数
# case_name_list = get_all_case_name()
case_name_list = ["新建工作日报","新建产品"]


# 执行所有Api接口用例
@pytest.mark.parametrize('case_name', case_name_list)
def test_run_all_case(case_name):
    basic.exe_case(case_name)
    basic.assert_result(case_name)

if __name__ == "__main__":
    pytest.main(["-s","--html=report.html","--alluredir=./report","test_run_pro_api.py::test_run_all_case"])