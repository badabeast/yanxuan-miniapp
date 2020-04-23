from pathlib import Path
import sys
PROJECT_PATH = Path(__file__).parent.parent
sys.path.append(str(PROJECT_PATH))
from utils.mongoconnect import MongoConnect
from utils.constant import Constant
from orm.ormdb import ApiRequestCase

MongoConnect()

def gen_render_data():
    try:
        defult_data = [
            ['当前分钟','字符串','','\"${time@current_minute}\"'],
            ['下一小时','字符串','','\"${time@next_hour}\"'],
            ['当天','字符串','','\"${time@today}\"'],
            ['明天','字符串','','\"${time@tomorrow}\"'],
            ['当月开始的第一天','字符串','','\"${time@month}\"'],
            ['Unix时间戳','时间戳','','\"${time@unix_format_now}\"'],
            ['当天零点的时间戳','时间戳','','\"${time@unix_today}\"'],
            ['前一天的时间戳','时间戳','','\"${time@unix_format_yesterday}\"'],
            ['明天0点的时间戳','时间戳','','\"${time@unix_format_tomorrow}\"'],
            ['人名','','','\"${faker@people_name}\"'],
            ['手机号','','','\"${faker@phone}\"'],
            ['颜色','','','\"${faker@color}\"']
        ]
        data = []
        request_cases = ApiRequestCase.objects().all()
        for request_case in request_cases:
            if len(request_case.key_need_to_save) > 0 :
                for k,v in request_case.key_need_to_save.items():
                    data.append([request_case.case_name,k,v,"\"${%s@%s}\"" % (request_case.case_name,k)])
        return defult_data + data
    except Exception as e:
        print(request_case.case_name)
    
from jinja2 import Environment,FileSystemLoader
env = Environment(loader=FileSystemLoader("./tests"))
tempalte = env.get_template("replace_param_tempalte.html")
content = tempalte.render(params=gen_render_data())

with open('./tests/目前支持替换的参数列表.html','w',encoding='utf-8') as f:
    f.write(content)