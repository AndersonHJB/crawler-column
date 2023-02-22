import requests
from lxml import etree
import random


class Spider16:
    def __init__(self):

        self.wait_urls = ["https://www.qunzou.com/xuexi/list_1_1.html"]
        self.url_template = "https://www.qunzou.com/xuexi/list_1_{num}.html"
        self.details = []

    def get_headers(self):
        uas = [
            "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
            "Mozilla/5.0 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)",
            "Baiduspider-image+(+http://www.baidu.com/search/spider.htm)",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 YisouSpider/5.0 Safari/537.36",
            "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "Mozilla/5.0 (compatible; Googlebot-Image/1.0; +http://www.google.com/bot.html)",
            "Sogou web spider/4.0(+http://www.sogou.com/docs/help/webmasters.htm#07)",
            "Sogou News Spider/4.0(+http://www.sogou.com/docs/help/webmasters.htm#07)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);",
            "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
            "Sosospider+(+http://help.soso.com/webspider.htm)",
            "Mozilla/5.0 (compatible; Yahoo! Slurp China; http://misc.yahoo.com.cn/help.html)"
        ]
        ua = random.choice(uas)
        headers = {
            "user-agent": ua,
            "referer": "https://www.baidu.com"
        }
        return headers

    # 生成待爬取页面
    def create_urls(self):
        headers = self.get_headers()
        page_url = self.wait_urls[0]
        res = requests.get(url=page_url, headers=headers, timeout=5)
        html = etree.HTML(res.text)
        # 提取总页码
        last_page = html.xpath("//span[@class='pageinfo']/strong[1]/text()")[0]

        # 生成待爬取页面
        for i in range(1, int(last_page) + 1):
            self.wait_urls.append(self.url_template.format(num=i))

    def get_html(self):
        for url in self.wait_urls:
            headers = self.get_headers()
            res = requests.get(url, headers=headers, timeout=5)
            if res:
                html = etree.HTML(res.text)
                detail_link_list = html.xpath("//div[@class='list']//h6/a/@href")
                for d in detail_link_list:
                    self.details.append(f"https://www.qunzou.com{d}")
                    # 测试用，直接 return
                    return

    def get_detail(self):
        for url in self.details:
            headers = self.get_headers()
            res = requests.get(url, headers=headers, timeout=5)
            res.encoding = "gb2312"
            if res:
                html = etree.HTML(res.text)
                sentences = html.xpath("//div[@id='content']//p/text()")
                # 打印句子
                long_str = "\n".join(sentences)

                print(long_str)
                # with open("sentences.txt", "a+", encoding="utf-8") as f:
                #     f.write(long_str)

    def run(self):
        self.create_urls()
        self.get_html()
        self.get_detail()


if __name__ == '__main__':
    s = Spider16()
    s.run()
