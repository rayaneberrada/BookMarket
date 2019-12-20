# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class MatchItem(scrapy.Item):
    home = scrapy.Field()
    away = scrapy.Field()
    sport = scrapy.Field()
    league = scrapy.Field()
    broadcasters = scrapy.Field()
    region = scrapy.Field()
    time_scraped = scrapy.Field()
    playing_time = scrapy.Field()
    bookmaker = scrapy.Field()
    odd_home = scrapy.Field()
    odd_away = scrapy.Field()
    odd_draw = scrapy.Field()

    #Housekeping fields
    url = scrapy.Field()