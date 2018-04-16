import urllib.request 
import json

req = urllib.request.Request('https://api.vk.com/method/wall.get?owner_id=1&count=10&v=5.74&access_token=b463f077b463f077b463f0777db401c10dbb463b463f077eeb7bd7554fac7a413df2e82') 
response = urllib.request.urlopen(req)
result = response.read().decode('utf-8')

data = json.loads(result)

print(type(data))
