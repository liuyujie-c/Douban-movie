# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()         # 电影名
    img_link = scrapy.Field()     # 电影海报链接
    score = scrapy.Field()        # 电影评分
    director = scrapy.Field()     # 导演
    commenter = scrapy.Field()    # 影评的用户名称
    comment = scrapy.Field()      # 影评

