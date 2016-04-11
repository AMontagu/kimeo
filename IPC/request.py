import requests

url = "http://172.17.97.210/api/"


class RequestsPost:
    def __init__(self, emailIn, passwordIn):
        self.email = emailIn
        self.password = passwordIn

    def postMessage(self, robotId, userName, content, created):
        payload = {'email': self.email, 'password': self.password, 'robotId': robotId, 'userName': userName, 'content': content, 'created': created}
        r = requests.post(url + 'messages/', data=payload)
        print(r.text)

    def testConnection(self):
        r = requests.get(url)
        print(r.status_code)
        print(r.text)