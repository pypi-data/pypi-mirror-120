import hashlib
import json
import time
from urllib.parse import urlencode
from kernel.config import Config
from kernel.context import Context
from Tea.response import TeaResponse

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8');
        return json.JSONEncoder.default(self, obj)

def merge(system_params, biz_params, text_params):
    biz_params.update(system_params)
    text_params.update(biz_params)
    return text_params

def sort_map(params):
    return sorted(params.items(), key=lambda x:x[0], reverse=False)

class Client:
    CODE = 'code'
    MSG = 'msg'
    SUCCESS_CODE = '200'
    BIZ_CONTENT_FIELD = 'business_data'
    DEFAULT_CHARSET = 'UTF-8'
    context = None
    def __init__(self,context):
       self.context = context
    def get_config(self,key):
        return self.context.get_config(key)

    def get_timestamp(self):
        return int(round(time.time() * 1000))

    def to_jsonstring(self,params):
        return json.dumps(params)

    def sort_map(self,params):
        return params

    def read_as_json(self,teaResponse):
        return json.loads(teaResponse.body.decode('utf-8'))

    def sign(self,system_params,biz_params,text_params,secret_key):
        mergeDic = merge(system_params,biz_params,text_params)
        # sorted_map = sort_map(mergeDic)
        encodeStr = self.build_query_string(mergeDic)
        encodeStr = encodeStr.replace('+','')
        x = hashlib.sha256()
        x.update((secret_key + encodeStr).encode('utf-8'))
        return x.hexdigest()

    def obj_to_jsonstring(self,obj):
        json_str = json.dumps(obj,default=lambda obj:obj.__dict__,sort_keys=True,indent=4)
        return json_str

    def to_resp_model(self,params):
        code = str(params[self.CODE])
        msg = str(params[self.MSG])
        if(code != None and code == self.SUCCESS_CODE):
            data = str(params[self.BIZ_CONTENT_FIELD])
            return json.loads(data)
        raise Exception('接口访问异常，code:{},msg:{}'.format(code,msg))
    def to_url_encoded_request_body(self,params):
        # sorted_map = sort_map(params)
        return self.build_query_string(params)
    def build_query_string(self,sorted_dict):
        keys = []

        for k in sorted_dict:
                keys.append(k)
        new_keys = sorted(keys)
        pList = []
        for i in new_keys :
            pList.append(str(i)+"="+str(sorted_dict[i]))
        requestUrl = '&'.join(pList)
        return requestUrl
if __name__ == '__main__':
    config = Config()
    config.secretKey = '111'
    context = Context(config)
    key = context.get_config('secretKey')
    print(key)
    client = Client(context)
    dic1 = {
	'signature': '05cc9ee5a48c264568c208547fcdf6f35546c30ee4598acfa4c99f233f8f21f3',
	'app_id': '4139937041702170912',
	'merchant_id': '87891',
	'access_token': 'efd83327-63a9-4e03-b913-1accbcc549b6',
	'timestamp': '1630500481740',
	'version': '1.0',
	'business_data': '{\"page_no\": \"1\", \"page_size\": \"20\", \"merchant_id\": \"87891\"}'
    }
    dic2 = {

    }
    dic3 = {

    }
    # teaResponse = TeaResponse()
    # teaResponse.headers = ''
    # JSONStr = client.read_as_json(TeaResponse)
    # print(JSONStr)
    params = {
        'code':'200',
        'msg':'系统内部错误',
        'business_data':'{"a": "1"}'
    }

    map = {
	'signature': '05cc9ee5a48c264568c208547fcdf6f35546c30ee4598acfa4c99f233f8f21f3',
	'app_id': '4139937041702170912',
	'merchant_id': '87891',
	'access_token': 'efd83327-63a9-4e03-b913-1accbcc549b6',
	'timestamp': '1630547616151',
	'version': '1.0',
	'business_data': '{\"page_no\": \"1\", \"page_size\": \"20\", \"merchant_id\": \"87891\"}'
    }
    map2 = {}
    map3 = {}

    # print(urlencode(sort_map(map),'utf-8'))
    # client.sort_map(params)
    # client.to_resp_model(params)
    # r = bytes(json.dumps(params),'utf-8')

    # print(r.decode('utf-8'))
    # content = client.build_query_string(params)
    # print(urlencode(params))
    my_params = {
        'page_no':'1',
        'page_size': '20',
        'merchant_id':'87891'

    }
    system_params = {
        'app_id': '4139937041702170912',
        'merchant_id':'87891',
        'access_token': 'efd83327-63a9-4e03-b913-1accbcc549b6',
        'timestamp': '1630547616151',
        'version': '1.0',
        'business_data': json.dumps(my_params).replace(' ','')
    }
    # content = client.build_query_string(system_params);
    dic4 = client.sign(system_params,map2,map3,"3badb149-67df-462e-9c57-683016d0a5d3")
    print(dic4)