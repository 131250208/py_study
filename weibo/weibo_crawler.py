# -*- coding:utf-8 -*-
import requests
import json
import logging
import time
import random

class WeiboCrawler:
    def random_wait(self, base, interval):
        random.seed(time.time())
        sleeptime = base + interval * random.random()
        print("sleep %ds" % sleeptime)
        time.sleep(sleeptime)

    def get_mids(self, uid, search=None, page_end=50):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip,deflate,br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Connection": "keep-alive",
            "Host": "weibo.com",
            "Upgrade-Insecure - Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
        }

        for page in range(page_end):
            while True:
                try:
                    self.random_wait(1, 3)
                    url = "https://m.weibo.cn/api/container/getIndex?type=uid&value=%s&containerid=107603%s&page=%d" % (
                        uid, uid, page + 1)
                    res = requests.get(url, headers)
                    cards = json.loads(res.text)["data"]["cards"]
                    for c in cards:
                        if c["card_type"] == 9 and search in c["mblog"]["text"]:
                            print("%s %s" % (c["mblog"]["mid"], c["mblog"]["text"]))

                    break
                except Exception as e:
                    logging.warning(str(e))
                    continue # 每个出错请求都再次尝试
if __name__ == "__main__":
    wbc = WeiboCrawler()
    wbc.get_mids("1713926427", "______")