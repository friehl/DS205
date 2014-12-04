# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YPReview(scrapy.Item):
    business_id = scrapy.Field()
    user_id = scrapy.Field()
    stars = scrapy.Field()
    date = scrapy.Field()
    text = scrapy.Field()
    votes = scrapy.Field()
    name = scrapy.Field()
    id = scrapy.Field()
    type = scrapy.Field()
    
