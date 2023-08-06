# URA Token Package

This is a small example to obtain URA API token. 

## Register for your access key with [URA](https://www.ura.gov.sg/maps/api/reg.html)

## Example:
```python
import requests
import json

from ura_token import ura_token

u=ura_token.ura_token('<place your ura token here>')

url="https://www.ura.gov.sg/uraDataService/invokeUraDS?service=Car_Park_Availability"
myobj = {'AccessKey': u.get_accesskey(), 'token': u.get_token(), 'User-Agent': 'Mozilla/5.0'}
resp = requests.post(url, headers=myobj)

print(json.dumps(resp.json()['Result'], indent=4))
```

Questions or bugs, please write to chengguan.teo@gmail.com.
