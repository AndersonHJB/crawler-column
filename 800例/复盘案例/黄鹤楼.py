import threading
import asyncio
import time
import requests
import lxml
from bs4 import BeautifulSoup


async def get(url):
    return requests.get(url)


async def get_html(url):
    print("准备抓取：", url)
    res = await get(url)
    return res.text


async def save_img(img_url):
    print("图片下载中：", img_url)
    res = await get(img_url)
    if res is not None:
        with open(f'./imgs/{time.time()}.jpg', 'wb') as f:
            f.write(res.content)
            return img_url,"ok"


async def main(url_list):
    # 创建 5 个任务
    tasks = [asyncio.ensure_future(get_html(url_list[_])) for _ in range(len(url_list))]

    dones, pending = await asyncio.wait(tasks)
    for task in dones:
        html = task.result()
        soup = BeautifulSoup(html, 'lxml')
        div_tag = soup.find(attrs={'class': 'lbox'})
        imgs = div_tag.find_all('img')


        for img in imgs:
            ret = await save_img(img["data-original"])
            print(ret)


if __name__ == '__main__':
    # 修改为黄鹤楼，测试方便，仅使用10页
    urls = [f"https://www.huanghelou.cc/category-44_{page}.html" for page in range(1, 10)]
    totle_page = len(urls) // 5 if len(urls) % 5 == 0 else len(urls) // 5 + 1
    # 对 urls 列表进行切片，方便采集
    for page in range(0, totle_page):
        start_page = 0 if page == 0 else page * 5
        end_page = (page + 1) * 5


        # 循环事件对象
        loop = asyncio.get_event_loop()

        loop.run_until_complete(main(urls[start_page:end_page]))
