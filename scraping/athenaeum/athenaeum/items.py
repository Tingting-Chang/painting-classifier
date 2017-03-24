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

class PaintingDownloadItem(Item):
    author_id = Field()
    painting_id = Field()
    painting_url = Field()
    
    def __init__(self, painting_item, *args, **kwargs):
        if isinstance(painting_item, PaintingItem):
            super(PaintingDownloadItem, self).__init__(*args, **kwargs)
            for key in ['author_id', 'painting_id', 'painting_url']:
                self[key] = painting_item[key]
        else:
            super(PaintingDownloadItem, self).__init__(painting_item, *args, **kwargs)
    
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
