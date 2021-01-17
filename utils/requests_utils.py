import requests
import ast
import re
import jsonpath
import json
from utils.config_utils import config

class RequestsUtils():
    def __init__(self):
        self.session = requests.session()
        self.url = config.get_url
        self.temp_dic = {}



    def __get_requests(self,requests_info):
        """
         :param requests_info: 传的是每个步骤的字典格式
         """
        #处理关联
        str_value = requests_info['请求参数(get)']     #requests_info['请求参数(get)'] 格式形如：'{"access_token":${token}}'
                                                      #temp_dic格式形如 {"token":"hdjhskjfskdf"}
        re_value = re.findall('\\${\w+}',str_value)
        for var in re_value:
            str_value = str_value.replace(var,'"%s"'%self.temp_dic[var[2:-1]])  #此处需要将字典中取出来的value加上双引号，所以用到格式化字符串
        # print(str_value)


        get_response = self.session.get(url = self.url + requests_info['请求地址'],
                                        params = ast.literal_eval(str_value))
        get_response.encoding = get_response.apparent_encoding

        if requests_info['取值方式'] == 'json取值':
            value = jsonpath.jsonpath(get_response.json(),requests_info['取值代码'])[0]
            self.temp_dic[requests_info['传值变量']] = value
        if requests_info['取值方式'] == '正则取值':
            value = re.findall(requests_info['取值代码'],get_response.text)[0]
            self.temp_dic[requests_info['传值变量']] = value


        result = {
            'code':0,
            'response_reason':get_response.reason,
            'response_status':get_response.status_code,
            'response_body':get_response.text,
            'response_headers':get_response.headers
        }
        return result



    def __post_requests(self,requests_info):
        """
         :param requests_info: 传的是每个步骤的字典格式
         """
        #处理关联
        str_value = requests_info['请求参数(get)']     #requests_info['请求参数(get)'] 格式形如：'{"access_token":${token}}'
                                                      #temp_dic格式形如 {"token":"hdjhskjfskdf"}
        re_value = re.findall('\\${\w+}',str_value)
        for var in re_value:
            str_value = str_value.replace(var,'"%s"'%self.temp_dic[var[2:-1]])  #此处需要将字典中取出来的value加上双引号，所以用到格式化字符串


        post_response = self.session.post(url = self.url + requests_info['请求地址'],
                                          params = json.loads(str_value),
                                          json =  json.loads(requests_info['提交数据（post）']))  # data传的参数是字符串形式，json传的是字典格式
        post_response.encoding = post_response.apparent_encoding

        if requests_info['取值方式'] == 'json取值':
            value = jsonpath.jsonpath(post_response.json(),requests_info['取值代码'])[0]
            self.temp_dic[requests_info['传值变量']] = value
        if requests_info['取值方式'] == '正则取值':
            value = re.findall(requests_info['取值代码'],post_response.text)[0]
            self.temp_dic[requests_info['传值变量']] = value

        result = {
            'code':0,
            'response_reason':post_response.reason,
            'response_status':post_response.status_code,
            'response_body':post_response.text,
            'response_headers':post_response.headers
        }
        return result


    def requests_combine(self,requests_info):
        """

        :param requests_info: 传的是每个步骤的字典格式
        :return:
        """
        if requests_info['请求方式'] == 'get':
            result = self.__get_requests(requests_info)
        elif requests_info['请求方式'] == 'post':
            result = self.__post_requests(requests_info)
        else:
            result = {
                'code':1,
                'error_msg':'请求方式不支持'
            }
        return result


    def case_step(self,case_steps):
        """
        将一个案例的多个步骤进行串联
        :param case_steps: 传入的数据格式是[{step1},{step2}...]
        :return:
        """
        result = None
        for step in case_steps:
            result = self.requests_combine(step)
            print(result['response_body'])
            if result['code'] != 0:
                break
        return result





if __name__ == '__main__':
    get_info = {'测试用例编号': 'case01',
            '测试用例名称': '测试能否正确执行获取access_token接口',
            '用例执行': '是',
            '测试用例步骤': 'step_01',
            '接口名称': '获取access_token接口',
            '请求方式': 'get',
            '请求地址': '/cgi-bin/token',
            '请求参数(get)': '{"grant_type":"client_credential","appid":"wx3465fb2ad43d9bb8","secret":"a940067445269e2f8549ddae17808ff6"}',
            '提交数据（post）': '',
            '取值方式': '无',
            '传值变量': '',
            '取值代码': '',
            '期望结果类型': 'json键是否存在',
            '期望结果': 'access_token,expires_in'}
    post_info = {

		'测试用例编号': 'case02',
		'测试用例名称': '测试能否正确新增用户标签',
		'用例执行': '否',
		'测试用例步骤': 'step_02',
		'接口名称': '创建标签接口',
		'请求方式': 'post',
		'请求地址': '/cgi-bin/tags/create',
		'请求参数(get)': '{"access_token":"41_SVv1e_cUcC5gKL8hdUzYJ-M6ixGF29NGVeoNMkUvefKGkYAGzGx9hcRk3eXBenIYb--d49cQaEjSqobw0UeY8i-8m0bChyPEa4tUChQWYiynBwe8l-Ss0wjIa4bgDDD9RNdaod-zhfnWzBLTSVEfACALOX"}',
		'提交数据（post）': '{"tag" : {"name" : "衡东8"}}',
		'取值方式': '无',
		'传值变量': '',
		'取值代码': '',
		'期望结果类型': '正则匹配',
		'期望结果': '{"tag":{"id":(.+?),"name":"衡东8"}}'
	}
    combine_info =  [{
            '测试用例编号': 'case02',
            '测试用例名称': '测试能否正确新增用户标签',
            '用例执行': '否',
            '测试用例步骤': 'step_01',
            '接口名称': '获取access_token接口',
            '请求方式': 'get',
            '请求地址': '/cgi-bin/token',
            '请求参数(get)': '{"grant_type":"client_credential","appid":"wx3465fb2ad43d9bb8","secret":"a940067445269e2f8549ddae17808ff6"}',
            '提交数据（post）': '',
            '取值方式': '正则取值',
            '传值变量': 'token',
            '取值代码': '"access_token":"(.+?)"',
            '期望结果类型': '正则匹配',
            '期望结果': '{"access_token":"(.+?)","expires_in":(.+?)}'
        }, {
            '测试用例编号': 'case02',
            '测试用例名称': '测试能否正确新增用户标签',
            '用例执行': '否',
            '测试用例步骤': 'step_02',
            '接口名称': '创建标签接口',
            '请求方式': 'post',
            '请求地址': '/cgi-bin/tags/create',
            '请求参数(get)': '{"access_token":${token}}',
            '提交数据（post）': '{"tag" : {"name" : "衡东4"}}',
            '取值方式': '无',
            '传值变量': '',
            '取值代码': '',
            '期望结果类型': '正则匹配',
            '期望结果': '{"tag":{"id":(.+?),"name":"衡东4"}}'
        }]

    requests_doc = RequestsUtils()
    # print(requests_doc.requests_combine(get_info))
    # print(requests_doc.requests_combine(post_info))
    print(requests_doc.case_step(combine_info))



