# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class JyeooCrawlItem(Item):
    # define the fields for your item here like:
    # name = Field()
    #question_txt = Field()
    type_html = Field()
    label_html = Field()
    question_html = Field()
    #ans_txt = Field()
    ans_html = Field()
    #parse_txt = Field()
    parse_html = Field()
    comments_html = Field()
    question_url = Field()
    pass

class JyeooCrawlLoader(ItemLoader):
    default_item_class = JyeooCrawlItem 
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    question_html_out = Join()
