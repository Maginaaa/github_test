# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose
from scrapy.loader.processors import Join

def parse_field(text):
    return str(text).strip()

class GithubTestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class EmailItem(scrapy.Item):

    # 邮箱
    email = scrapy.Field(
        input_processor=MapCompose(parse_field),
        output_processor=Join(),
    )

