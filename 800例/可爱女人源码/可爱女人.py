import requests
import re
import threading
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}

# 详情页图片地址 URL
detail_urls = []

mutex = threading.Lock()


# 循环获取URL
def get_detail_urls(url):
    res = requests.get(url=url, headers=headers)
    res.encoding = 'gb2312'
    if res is not None:

        html = res.text  # 读取页面源码
        # 对目标源码页数据进行裁剪
        # 获取 ul class = "g-gxlist-imgbox" 的数据
        # 该数据在标签 <ul class="g-gxlist-imgbox"> 和 <div class="pagelist"> 之间
        html = html[html.find('<ul class="g-gxlist-imgbox">'):html.find('<div class="pagelist">')]
        # 裁剪之后的数据，可以使用正则提取
        # 设置正则表达式对象
        pattern = re.compile('<a href="(.*?)" target="_blank" title=".*?">')
        # 提取详情页地址
        find_urls = pattern.findall(html)

        if find_urls:
            # 上锁
            mutex.acquire()
            # 添加到全局变量中
            detail_urls.extend(find_urls)
            # 释放锁
            mutex.release()


# 保存图片线程
def save_image():
    global detail_urls

    while True:
        # 上锁
        mutex.acquire()
        if len(detail_urls) > 0:
            # 获取列表第1项
            img_url = detail_urls[0]
            # 删除列表第1项
            del detail_urls[0]
            # 释放锁
            mutex.release()
            res = requests.get(url=img_url, headers=headers)

            if res is not None:
                html = res.text

                # 裁切目标源码，便于后续整体提取
                html = html[html.find('<div class="img-list3">'):html.find('<div class="m_ssxx">')]
                pattern = re.compile('<img alt=".*?" src="(.*?)" />')

                img_list = pattern.findall(html)

                if img_list:
                    for img in img_list:
                        print(f"线程{threading.currentThread().name}", "抓取图片中：", img)

                        try:
                            res = requests.get(img)
                            with open(f"images/{threading.currentThread().name + str(time.time())}.png", "wb+") as f:
                                f.write(res.content)
                        except Exception as e:
                            print(e)
        else:
            print("等待中，长时间等待，可以直接关闭")


if __name__ == '__main__':
    # 生成分页地址
    origin_url = ['http://www.imeitou.com/nvsheng/']
    for i in range(2, 11):
        origin_url.append(f'http://www.imeitou.com/nvsheng/index_{i}.html')

    # 获取图片详情页地址
    for d_url in origin_url:
        get_detail_urls(d_url)

    # 测试得到的详情页地址列表
    # 测试得到 160 条地址，数据量是正确的
    print(len(detail_urls))

    # 保存图片线程配置+启动
    # 这里我们开启2个线程
    save1 = threading.Thread(target=save_image)
    save1.start()

    save2 = threading.Thread(target=save_image)
    save2.start()
