import urllib.request
import urllib.error
import json
import base64
import typing

class UbisoftAPIError(Exception):
    def __init__(self, caught=None):
        self.caught = caught

class UbisoftAPI(object):
    LOGIN_ENDPOINT = "https://uplayconnect.ubi.com/ubiservices/v2/profiles/sessions"
    APP_ID = "39baebad-39e5-4552-8c25-2c9b919064e2"
    __auth_response = None
    ticket = None

    def __init__(self, username: str, password: str):
        #We can try and use the built in Base64 Authenticator, however it doesn't appear to be
        #possible to set headers, so instead we can just do it this way.
        b64_credentials = base64.b64encode(("%s:%s" % (username, password)).encode('utf-8'))

        header = {
            "Content-Type":  "application/json",
            "Ubi-AppId":     UbisoftAPI.APP_ID,
            "Authorization": "Basic " + b64_credentials.decode('utf-8')
        }

        request = urllib.request.Request(UbisoftAPI.LOGIN_ENDPOINT,
                                        method="POST",
                                        headers=header,
                                        data=json.dumps(
                                            {
                                                "rememberMe": True
                                            }
                                        ).encode('utf-8'))
        try:
            response = urllib.request.urlopen(request)
            
            try:
                response_data = json.loads(response.read().decode('utf-8'))
                self.__auth_response = response_data
                self.ticket = self.__auth_response["ticket"]

            except json.JSONDecodeError as e:
                raise UbisoftAPIError(e)
                
        except urllib.error.HTTPError as e:
            raise UbisoftAPIError(e)

if __name__ == '__main__':
    try:
        ubisoft_api = UbisoftAPI("<username>", "<password>")
        print(ubisoft_api.ticket)
    except UbisoftAPIError as e:
        print(e.caught)