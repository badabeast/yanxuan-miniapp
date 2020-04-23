from pathlib import Path
import sys,pprint
PROJECT_PATH = Path(__file__).parent.parent
sys.path.append(str(PROJECT_PATH))
from orm.ormdb import ApiRequestCase,ApiCase,ApiCaseTemp
from utils.mongoconnect import MongoConnect

default_connection = MongoConnect()

requset_cases = ApiRequestCase.objects().all()
for requset_case in requset_cases:
    if ApiCase.objects(cid=requset_case.api_id).first():
        pass
    else:
        temp = ApiCaseTemp.objects(cid=requset_case.api_id).first()
        if temp:
            ApiCase(cid=temp.cid,method=temp.method,url=temp.url,comment=temp.comment,api_type=temp.api_type,business_module=temp.business_module).save()
        else:
            raise Exception("临时库也没这个url")