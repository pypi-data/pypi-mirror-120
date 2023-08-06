import requests
import json

from ura_token import ura_token

u=ura_token.ura_token('<place your ura access key here>')

url="https://www.ura.gov.sg/uraDataService/invokeUraDS?service=Car_Park_Availability"
myobj = {'AccessKey': u.get_accesskey(), 'token': u.get_token(), 'User-Agent': 'Mozilla/5.0'}
resp = requests.post(url, headers=myobj)

print(json.dumps(resp.json()['Result'], indent=4))
