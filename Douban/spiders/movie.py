# -*- coding: utf-8 -*-
import scrapy
import json
import re
import time
import random
from Douban.items import DoubanItem


class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/j/search_subjects?type=movie&tag=%E8%B1%86%E7%93%A3%E9%AB%98%E5%88%86&sort=rank&page_limit=20&page_start=0']

    def parse(self, response):
        el_list = json.loads(response.body.decode())["subjects"]
        for el in el_list:
            item = DoubanItem()
            item["name"] = el["title"]
            item["img_link"] = el["cover"]
            item["score"] = el["rate"]

            details_url = el["url"]
            yield scrapy.Request(url=details_url, callback=self.parse_details, meta={"item": item})

        ajax_url = response.request.url.rsplit("=", 1)
        ajax_url = "=".join([ajax_url[0], str(int(ajax_url[-1]) + 20)])
        time.sleep(random.random() * 2)
        yield scrapy.Request(url=ajax_url, callback=self.parse)

    def parse_details(self, response):
        # 处理电影详情页面
        item = response.meta["item"]
        item["director"] = response.xpath('//*[@id="info"]/span[1]/span[2]/a/text()').extract_first()

        comment_page_url = response.request.url + response.xpath('//*[@id="reviews-wrapper"]/p/a/@href').extract_first()
        yield scrapy.Request(url=comment_page_url, callback=self.parse_comment, meta={"item1": item})

    def parse_comment(self, response):
        # 处理评论页面
        el_list = response.xpath('//*[@id="content"]/div/div[1]/div[1]/div')
        for el in el_list:
            data = el.xpath("./@data-cid").extract_first()
            comment_details_url = "https://movie.douban.com/j/review/" + data + "/full"
            yield scrapy.Request(url=comment_details_url, callback=self.paesr_comment_details, meta=response.meta)

        # 翻页
        href = response.xpath('//*[@id="content"]/div/div[1]/div[2]/span[4]/a/@href').extract_first()
        if href:
            next_page_comment_url = response.urljoin(href)
            time.sleep(random.random() * 2)
            yield scrapy.Request(url=next_page_comment_url, callback=self.parse_comment, meta=response.meta)

    def paesr_comment_details(self, response):
        # 处理评论详情页面
        item = response.meta["item1"]
        data = json.loads(response.body.decode())
        item["commenter"] = re.findall('data-author=\"(.+)\"', data["body"])[0]
        item["comment"] = data["html"]
        yield item






