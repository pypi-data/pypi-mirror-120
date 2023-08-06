# get_ura_token.py
# 19 May 2020
#
# Register for your access key here: https://www.ura.gov.sg/maps/api/reg.html
# Questions or bugs, please write to chengguan.teo@gmail.com.
import requests

class ura_token:

    def __init__(self, accesskey, verbose=False):
        url = 'https://www.ura.gov.sg/uraDataService/insertNewToken.action'
        myobj = {'AccessKey': accesskey, 'User-Agent': 'Mozilla/5.0'}

        self.accesskey = accesskey
        self.token = None

        # Place the access key in the request header and send.
        resp = requests.post(url, headers=myobj)

        if (resp.status_code==200):
            try:
                result = resp.json()['Result']
                self.token = result
                if verbose:
                    print(f"Token: '{result}'.")
            except:
                if verbose:
                    print(f'{resp.text}') # print error msg (should the resp data structure changed...)
        else:
            if verbose:
                print(f'{resp.status_code=}: {resp.text}') # print error msg

    def get_token(self):
        return self.token

    def get_accesskey(self):
        return self.accesskey
