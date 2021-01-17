import re

dict1 = {'token':'bsdvfbbfjbb'}
str1 = '{"access_token":${token}}'

v1 = re.findall('\\${\w+}',str1)[0]
v2 = str1.replace(v1,dict1[v1[2:-1]])
print(v2)



dict2 = {'token1':'bsdvfbbfjbb','name':'liujingling'}
str2 = '{"access_token":${token1},"xingming":${name}}'
v2 = re.findall('\\${\w+}',str2)
for i in v2:
    str2 = str2.replace(i,'"%s"'%dict2[i[2:-1]])
print(str2)

