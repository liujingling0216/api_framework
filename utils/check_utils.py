import json
import re

class CheckUtils:
    def __init__(self,response=None):
        self.response = response
        self.rules = {
            '无': self.no_check,
            'json键是否存在':self.key_check,
            'json键值对':self.keyvalue_check,
            '正则匹配':self.rex_check
        }

    def no_check(self,check_data=None):
        return True

    def key_check(self,check_data):
        expect_key_list = check_data.split(',')
        acture_dic = json.loads(self.response)
        temp_result = []
        for check_key in expect_key_list:
            if check_key in acture_dic.keys():
                temp_result.append(True)
            else:
                temp_result.append(False)
        if False in temp_result:
            return False
        else:
            return True

    def keyvalue_check(self,check_data):
        acture_dic1 = json.loads(self.response)
        expect_dic = json.loads(self,check_data)
        temp_result1 = []
        for v in acture_dic1.items():
            if v in expect_dic.items():
                 temp_result1.append('True')
            else:
                 temp_result1.append('False')
        if True in temp_result1:
            result = True
        else:
            result = False
        return result

    def rex_check(self,check_data):
        if re.findall(check_data, self.response):
            result = True
        else:
            result = False
        return result

if __name__ == '__main__':
    response = {
	'测试用例编号': 'case01',
	'请求地址': '/cgi-bin/token',
	'提交数据（post）': '',
	'取值代码': '',
	'测试用例步骤': 'step_01',
	'接口名称': '获取access_token接口',
	'传值变量': '',
	'请求方式': 'get',
	'请求参数(get)': '{"grant_type":"client_credential","appid":"wx3465fb2ad43d9bb8","secret":"a940067445269e2f8549ddae17808ff6"}',
	'期望结果类型': 'json键是否存在',
	'用例执行': '是',
	'取值方式': '无',
	'测试用例名称': '测试能否正确执行获取access_token接口',
	'期望结果': 'access_token,expires_in'
}
    test_doc = CheckUtils(json.dumps(response)).key_check()
    print(test_doc)







