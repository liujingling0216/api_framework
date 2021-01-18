import re
import json

acture = '{"access_token":"mLauwmQxSce0b77znKyLxWDOztJUNHDlTxR-ttZlsOEkRUBbAGAHKR","expires_in":7200}'

expect1 = '{"access_token":"(.+?)","expires_in":(.+?)}'
expect2 = 'access_token,expires_in'
expect3 = '{"expires_in":7200}'

# 正则匹配
if re.findall(expect1,acture):
    result = True
else:
    result = False
# print(result)

# 键匹配
expect2_key_list = expect2.split(',')
acture_dic = json.loads(acture)
temp_result = []
for check_key in expect2_key_list:
    if check_key in acture_dic.keys():
        temp_result.append(True)
    else:
        temp_result.append(False)
# if False in temp_result:
#     print(False)
# else:
#     print(True)

# 键值匹配
acture_dic = json.loads(acture)
expect3_dic = json.loads(expect3)
temp_result1 = []
for v in acture_dic.items():
    if v in  expect3_dic.items():
        result = temp_result1.append('True')
    else:
        result = temp_result1.append('False')
if 'True' in temp_result1:
    result = True
else:
    result = False
print(result)









