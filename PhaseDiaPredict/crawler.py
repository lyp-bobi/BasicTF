import re
import requests
import datetime
import time
import urllib

url = "https://matdata.asminternational.org/apd/datasheet.aspx?search=true&record=384319&dbKey=grantami_apd"
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'}

unix_time=time.mktime(datetime.datetime.now().timetuple())
data = bytes(urllib.parse.urlencode({'now':unix_time}), encoding='utf8')

req = urllib.request.Request(url,headers=header,data=data)
response = urllib.request.urlopen(req)
print(response.read().decode('utf-8'))