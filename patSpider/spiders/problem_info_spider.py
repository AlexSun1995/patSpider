# -*- coding:utf-8 -*-
from scrapy import FormRequest
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider
from patSpider.items import *
import pickle
from patSpider.pipelines import *

class pat_Spider(CrawlSpider):
    name = "pat"
    items = []
    call_times = 0
    # allowed_domains = []
    start_urls = ["https://www.patest.cn/contests/pat-a-practise",
                  "https://www.patest.cn/contests/pat-a-practise?page=2"
                  ]

    def start_requests(self):
        return [Request("https://www.patest.cn/users/sign_in", meta={'cookiejar': 1}, callback=self.post_login)]

    def post_login(self, response):
        post_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36",
            "Referer": "https://www.patest.cn/users/sign_in",
            "Upgrade-Insecure-Requests": 1

        }
        authenticity_token = response.xpath('//input[@name="authenticity_token"]/@value').extract()[0]
        # print authenticit-y_token
        return [FormRequest.from_response(response,
                                          url="https://www.patest.cn/users/sign_in",
                                          meta={'cookiejar': response.meta['cookiejar']},
                                          headers=post_headers,
                                          formdata={
                                              'utf8': '✓',
                                              'authenticity_token': authenticity_token,
                                              'user[handle]': 'suncun',
                                              'user[password]': '13856359787',
                                              'user[remember_me]': '0',
                                              'commit': "登录"
                                          },
                                          callback=self.after_login,
                                          dont_filter=True
                                          )]


    def after_login(self, response):
        for url in self.start_urls:
            yield Request(url, meta={'cookiejar': response.meta['cookiejar']})


    def parse(self, response):
        print response.body
        self.call_times += 1
        data_selector = response.xpath('//tr/td')
        i = 0
        while i < len(data_selector):
            six_lines = data_selector[i:i+6 ]
            i += 6
            item = PatspiderItem()
            if len(six_lines[0].xpath('.//span/text()').extract()) == 0:
                item['does_pass'] = 'Not submit'
            else:
                item['does_pass'] = six_lines[0].xpath('.//span/text()').extract()[0]
            item['id'] = six_lines[1].xpath('.//a/text()').extract()[0]
            item['title'] = six_lines[2].xpath('.//a/text()').extract()[0]
            item['pass_times'] = six_lines[3].xpath('./text()').extract()[0]
            item['submit_times'] = six_lines[4].xpath('./text()').extract()[0]
            item['pass_rate'] = six_lines[5].xpath('./text()').extract()[0]
            self.items.append(item)
            # do not use 'return' cause the item is piped to 'pipelines'
            # when the Spider is working. yield can make data collecting and
            # processing at the same time.
            yield item
        if self.call_times == len(self.start_urls):
            with open('items_list', 'wb') as tmp_f:
                pickle.dump(self.items, tmp_f)