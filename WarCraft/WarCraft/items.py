# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Heros(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    type = ['Strength','Agility','Intelligence']
    name = scrapy.Field()
    ability = scrapy.Field()
    counter = scrapy.Field()
    good_against = scrapy.Field()
    work_well_with = scrapy.Field()



