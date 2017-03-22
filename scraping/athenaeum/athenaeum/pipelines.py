# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import CsvItemExporter
from athenaeum.items import AuthorItem, PaintingItem

DATA_PATH = '../../data/'

class AuthorPipeline(object):
    filename = DATA_PATH + 'athenaeum_authors.csv'
    
    def open_spider(self, spider):
        self.csvfile = open(self.filename, 'wb')

        self.exporter = CsvItemExporter(self.csvfile)
        self.exporter.start_exporting()
    
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.csvfile.close()
    
    def process_item(self, item, spider):
        if isinstance(item, AuthorItem):
            for key in item:
                if isinstance(item[key], unicode):
                    item[key] = item[key].encode('utf-8')
            self.exporter.export_item(item)
        return item

class PaintingPipeline(object):
    filename = DATA_PATH + 'athenaeum_paintings.csv'
    
    def open_spider(self, spider):
        self.csvfile = open(self.filename, 'wb')

        self.exporter = CsvItemExporter(self.csvfile)
        self.exporter.start_exporting()
    
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.csvfile.close()
    
    def process_item(self, item, spider):
        if isinstance(item, PaintingItem):
            for key in item:
                if isinstance(item[key], unicode):
                    item[key] = item[key].encode('utf-8')
            self.exporter.export_item(item)
        return item
