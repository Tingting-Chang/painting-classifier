# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class PaintingItem(Item):
    author_id = Field()
    painting_id = Field()
    painting_title = Field()
    painting_url = Field()
    painting_location = Field()
    painting_dates = Field()
    height = Field()
    height_uom = Field()
    width = Field()
    width_uom = Field()
    article_type = Field()
    medium = Field()
    image_out = Field()
    
class AuthorItem(Item):
    author_id = Field()
    last_name = Field()
    first_name = Field()
    bio_url = Field()
    nationality = Field()
    birth_year = Field()
    death_year = Field()
    art_movement = Field()
    bio_info = Field()
