# import requests
#
# response = requests.get("https://www.uisdc.com/archives")
# content = response.text
#
# with open("ca_demo.html", "w") as file:
#     file.write(content)
import urllib.parse
decoded = urllib.parse.unquote("%3Ci+class%3D%22uname%22+title%3D%22%E4%BC%98%E7%A7%80%E7%BD%91%E9%A1%B5%E8%AE%BE%E8%AE%A1%22%3E%E4%BC%98%E7%A7%80%E7%BD%91%E9%A1%B5%E8%AE%BE%E8%AE%A1%3C%2Fi%3E")
print(decoded)