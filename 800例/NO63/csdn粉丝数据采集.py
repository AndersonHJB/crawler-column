import json


class GetFans(object):
    def response(self, flow):
        start_url = "https://blog.csdn.net/community/home-api/v1/get-fans-list"

        response = flow.response
        if flow.request.url.startswith(start_url):
            text = response.text
            data = json.loads(text)
            print(data)

addons = [
    GetFans()
]
