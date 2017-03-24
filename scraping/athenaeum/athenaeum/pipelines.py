# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import CsvItemExporter
from scrapy import Request
from athenaeum.items import AuthorItem, PaintingItem, PaintingDownloadItem
from scrapy.pipelines.images import ImagesPipeline
from athenaeum import settings
from PIL import Image
import os
try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

class AthenaeumBaseCSVPipeline(object):
    # filename = ??
    # class_to_filter = ??
    
    def open_spider(self, spider):
        create = not os.path.exists(self.filename)
        self.csvfile = open(self.filename, 'ab')

        self.exporter = CsvItemExporter(self.csvfile, include_headers_line = create)
        self.exporter.start_exporting()
    
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.csvfile.close()
    
    def process_item(self, item, spider):
        if isinstance(item, self.class_to_filter):
            for key in item:
                if isinstance(item[key], unicode):
                    item[key] = item[key].encode('utf-8')
            self.exporter.export_item(item)
        return item

class AuthorPipeline(AthenaeumBaseCSVPipeline):
    filename = settings.DATA_PATH + 'athenaeum_authors.csv'
    class_to_filter = AuthorItem

class PaintingPipeline(AthenaeumBaseCSVPipeline):
    filename = settings.DATA_PATH + 'athenaeum_paintings.csv'
    class_to_filter = PaintingItem

class PaintingDownloadPipeline(ImagesPipeline):
    
    def get_media_requests(self, item, info):
        if isinstance(item, PaintingDownloadItem) or isinstance(item, PaintingItem):
            requests = [Request(item['painting_url'], meta = {'author_id': item['author_id'],
                            'painting_id': item['painting_id']})]
            info.spider.logger.debug('Sending image download request: %s' % str(requests))
            return requests
        else:
            return []
    
    def file_path(self, request, response=None, info=None):
        meta = request.meta
        return self.athenaeum_file_path(meta['author_id'], meta['painting_id'])
    
    def thumb_path(self, request, thumb_id, response=None, info=None):
        meta = request.meta
        return self.athenaeum_file_path(meta['author_id'], meta['painting_id'], thumb_id)
    
    # original implementation generates thumbnails by calling Image.thumbnail(),
    # while we're interested in Image.resize()
    def convert_image(self, image, size=None):
        if image.format == 'PNG' and image.mode == 'RGBA':
            background = Image.new('RGBA', image.size, (255, 255, 255))
            background.paste(image, image)
            image = background.convert('RGB')
        elif image.mode != 'RGB':
            image = image.convert('RGB')

        if size:
            image = image.resize(size, Image.LANCZOS)

        buf = BytesIO()
        image.save(buf, 'JPEG')
        return image, buf
        
    def item_completed(self, results, item, info):
        if isinstance(item, PaintingItem) and (len(results) == 0 or not results[0][0]):
            info.spider.logger.error('Unable to download picture id=%d: %s' % (item['painting_id'],
                            results[0][1] if len(results) > 0 else ''))
        return item
    
    @staticmethod
    def athenaeum_file_path(author_id, painting_id, thumb_id = None):
        if thumb_id is None:
            thumb_id = 'full'
        return '%s/%d/%d.jpg' % (thumb_id, author_id, painting_id)
