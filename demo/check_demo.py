import re

acture = '{"access_token":"mLauwmQxSce0b77znKyLxWDOztJUNHDlTxR-ttZlsOEkRUBbAGAHKR","expires_in":7200}'

expect1 = '{"access_token":"(.+?)","expires_in":(.+?)}'
expect2 = 'access_token,expires_in'
expect3 = '{"expires_in":7200}'

result1 = re.findall(expect1,acture)[0]
print(result1)

