import requests
import re




# 获取分页
def get_pagesize(html):
    # 编写简单的正则表达式 <a href='68_(\d+).html'>末页</a>
    pagesize = re.search("<a href='68_(\d+).html'>末页</a>", html)
    if pagesize is not None:
        return pagesize.group(1)
    else:
        return 0


# 获取待抓取列表
def get_wait_list(url):
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Proxy-Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Host": "p.ik123.com",
        "Referer": "http://p.ik123.com/",
    }
    wait_urls = []
    # try:
    res = requests.get(url=url, headers=HEADERS, timeout=5)
        # print(res)
    # res.encoding = "gb2312"
    html_text = res.text
    print("Xx", html_text)
        # pagesize = int(get_pagesize(html_text))
        # if pagesize > 0:
        #     print(f"获取到{pagesize}页数据")
            # 生成待抓取列表
            # for i in range(1, pagesize + 1):
            #     wait_urls.append(f"http://p.ik123.com/zt/maomi/68_{i}.html")
        # return wait_urls
    #
    # except Exception as e:
    #     print("异常", e)


if __name__ == '__main__':
    start_url = "http://p.ik123.com/zt/maomi/68_1.html"
    wait_urls = get_wait_list(url=start_url)
    print(wait_urls)