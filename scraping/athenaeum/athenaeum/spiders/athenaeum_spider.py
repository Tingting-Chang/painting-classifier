# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from athenaeum.items import PaintingItem, AuthorItem, PaintingDownloadItem
from athenaeum.pipelines import PaintingPipeline, AuthorPipeline, PaintingDownloadPipeline
from athenaeum.settings import IMAGES_STORE
#from athenaeum.settings import DATA_PATH, DOWNLOAD_DELAY
import re, sys, urllib, os, time#, threading
#from concurrent.futures import ThreadPoolExecutor
import pandas as pd

class AthenaeumSpiderSpider(Spider):
    name = "athenaeum-spider"
    allowed_domains = ["the-athenaeum.org"]
    start_urls = ['http://www.the-athenaeum.org/art/counts.php?s=cd&m=a']
    #images_folder = 'images_athenaeum'

    def __init__(self, *args, **kwargs):
        super(AthenaeumSpiderSpider, self).__init__(*args, **kwargs)
        #self.photo_downloader = ThreadPoolExecutor(max_workers = 1)
        self.scraped_artists = set()
        self.scraped_paintings = set()
        if os.path.exists(AuthorPipeline.filename):
            df = pd.read_csv(AuthorPipeline.filename)
            for author_id in df['author_id']:
                self.scraped_artists.add(author_id)
            self.logger.debug('Found %d artists already scraped.' % len(self.scraped_artists))
        if os.path.exists(PaintingPipeline.filename):
            for df in pd.read_csv(PaintingPipeline.filename, chunksize = 10000):
                for author_id, painting_id in zip(df['author_id'], df['painting_id']):
                    self.scraped_paintings.add((author_id, painting_id))
            self.logger.debug('Found %d paintings already scraped.' % len(self.scraped_paintings))
        if df is not None:
            del df
    
    #def __del__(self):
        #self.photo_downloader.shutdown()
        #super(AthenaeumSpiderSpider, self).__del__()
    
    def parse(self, response):
        for row in response.xpath('/html/body/div[@id="wrapper_no_sb_1024"]/table[1]//tr[(@class = "r1" or @class = "r2") and child::td[3]/@class = "pd"]'):
            try:
                tds = row.xpath('td')
                author = AuthorItem()
                names = re.sub(r'\s\s+', ' ', tds[0].xpath('a/text()').extract_first()).strip().split(', ', 1)
                last_name = names[0]
                last_name = last_name[0] + last_name[1:].lower()
                first_name = names[1] if len(names) > 1 else ''
                author['last_name'], author['first_name'] = last_name, first_name
                bio_url = response.urljoin(tds[0].xpath('a/@href').extract_first())
                author['bio_url'] = bio_url
                nationalityMatch = re.match(r'(.+), \d+', tds[1].xpath('text()').extract_first())
                nationality = nationalityMatch.group(1) if nationalityMatch is not None else None
                author['nationality'] = nationality
                yearMatch = re.match(r'(?:.+, )?(\d{2,4})-(\d{2,4}|\s*\?)', tds[1].xpath('text()').extract_first())
                birth_year = int(yearMatch.group(1))
                death_year = yearMatch.group(2).strip()
                death_year = int(death_year) if death_year.find('?') < 0 else None
                # Because of GIHON, Clarence Mon(t)fort
                if birth_year < 100:
                    birth_year += 1800
                    death_year += 1900
                author['birth_year'], author['death_year'] = birth_year, death_year
                movementMatch = re.match(r'.+\((.+)\)', tds[1].xpath('text()').extract_first())
                art_movement = movementMatch.group(1) if movementMatch is not None else None
                author['art_movement'] = art_movement
                art_list_url = response.urljoin(tds[2].xpath('a/@href').extract_first())
                author['author_id'] = int(re.match(r'.*\?ID=(\d+)$', tds[0].xpath('a/@href').extract_first()).group(1))
                
                if author['author_id'] not in self.scraped_artists:
                    yield Request(bio_url, meta = {'author_item': author}, callback = self.parse_bio)
                
                yield Request(art_list_url, meta = {'author_id': author['author_id']}, callback = self.parse_art_list_starter)
                
            except BaseException as e:
                self.logger.error('Unable to parse row: ' + row.extract() + '\n' + str(e))
    
    def parse_bio(self, response):
        author = response.meta['author_item']
        author['bio_info'] = '\n'.join([''.join(x.xpath('descendant-or-self::text()').extract())
                                        for x in response.xpath('//div[@id="topcontent"]/table/tr[1]/td[2]/p')])
        yield author
    
    def parse_art_list_starter(self, response):
        other_pages = response.xpath('/html/body/div[@id="wrapper_no_sb_1024"]/div[@class="subtitle"]/a')
        # for authors with only 1 painting/item
        if not other_pages and response.xpath('//div[@id="scholar"]/div[@id="generalInfo"]/table'):
            painting_id = int(re.match(r'.*\?ID=(\d+)&msg', response.url).group(1))
            not_in_csv = (response.meta['author_id'], painting_id) in self.scraped_paintings
            not_downloaded = not os.path.exists(os.path.join(IMAGES_STORE,
                            PaintingDownloadPipeline.athenaeum_file_path(response.meta['author_id'], painting_id)))
            if not_in_csv or not_downloaded:
                response.meta['store_to_csv'] = not_in_csv
                for elem in self.parse_painting(response):
                    yield elem
            return
        
        for elem in self.parse_art_list(response):
            yield elem
        
        if other_pages:
            urlMatch = re.match(r'(.*p=)(\d+)$', other_pages[-1].xpath('@href').extract_first())
            base_url = urlMatch.group(1)
            total_pages = int(urlMatch.group(2))
            for page_num in range(2, total_pages + 1):
                yield Request(response.urljoin(base_url + str(page_num)), meta = {'author_id': response.meta['author_id']},
                              callback = self.parse_art_list)
    
    def parse_art_list(self, response):
        for row in response.xpath('/html/body/div[@id="wrapper_no_sb_1024"]/table[1]//tr[@class = "r1" or @class = "r2"]'):
            try:
                url = row.xpath('td[2]/div[@class="list_title"]/a/@href').extract_first()
                painting_id = int(re.match(r'.*\?ID=(\d+)$', url).group(1))
                not_in_csv = (response.meta['author_id'], painting_id) not in self.scraped_paintings
                not_downloaded = not os.path.exists(os.path.join(IMAGES_STORE,
                            PaintingDownloadPipeline.athenaeum_file_path(response.meta['author_id'], painting_id)))
                if not_in_csv or not_downloaded:
                    yield Request(response.urljoin(url),
                                  meta = {'author_id': response.meta['author_id'], 'store_to_csv': not_in_csv},
                                  callback = self.parse_painting)
            except BaseException as e:
                self.logger.error('Unable to parse article row: ' + row.extract_first() + '\n' + str(e))
    
    def parse_painting(self, response):
        painting = PaintingItem()
        painting['author_id'] = response.meta['author_id']
        painting['painting_id'] = int(re.match(r'.*\?ID=(\d+)(?:&msg.*)?$', response.url).group(1))
        painting['painting_title'] = response.xpath('//div[@id="title"]/text()').extract_first()
        painting['painting_url'] = response.urljoin(response.xpath('//a[child::div/@class="subtitle_10px"]/@href').extract_first())
        for row in response.xpath('//div[@id="scholar"]/div[@id="generalInfo"]/table/tr'):
            key = row.xpath('td[1]/text()').extract_first()
            if key == 'Owner/Location:':
                painting['painting_location'] = row.xpath('td[2]/text()').extract_first().strip()
            elif key == 'Dates:':
                painting['painting_dates'] = row.xpath('td[2]/text()').extract_first().strip()
            elif key == 'Dimensions:':
                height_width_match = re.match(r'Height: (\d+\.?\d*) (.?m).*, Width: (\d+\.?\d*) (.?m)',
                                              row.xpath('td[2]/text()').extract_first().strip())
                if height_width_match is not None:
                    painting['height'] = float(height_width_match.group(1))
                    painting['height_uom'] = height_width_match.group(2)
                    painting['width'] = float(height_width_match.group(3))
                    painting['width_uom'] = height_width_match.group(4)
                elif row.xpath('td[2]/text()').extract_first().strip() != 'Unknown':
                    self.logger.warning('Unrecognized dimension format at id=%d: %s' % (painting['painting_id'],
                                                        row.xpath('td[2]/text()').extract_first().strip()))
            elif key == 'Medium:':
                medium = row.xpath('td[2]/text()').extract_first().strip().split(' - ')
                painting['article_type'] = medium[0].strip()
                painting['medium'] = medium[1].strip() if len(medium) > 1 else None
            elif key != 'Artist age:' and key != 'Entered by:':
                self.logger.warning('Article info key not parsed at id=%d: %s' % (painting['painting_id'], key))
        
        yield painting if response.meta['store_to_csv'] else PaintingDownloadItem(painting)
        #self.photo_downloader.submit(self.download_painting, painting['painting_url'],
                                     #painting['author_id'], painting['painting_id'])
    
    #def download_painting(self, url, author_id, painting_id):
        #local_directory = DATA_PATH + self.images_folder + '/%d/' % author_id
        #if not os.path.exists(local_directory):
            #os.makedirs(local_directory)
        #local_address = local_directory + '%d.jpg' % painting_id
        #try:
            #timer_thread = threading.Thread(target = time.sleep, args = (DOWNLOAD_DELAY / 2.0,))
            #timer_thread.start()
            #urllib.urlretrieve(url, local_address)
            #timer_thread.join(DOWNLOAD_DELAY)
        #except BaseException as e:
            #self.logger.error('Unable to download painting author=%d, id=%d: %s' % (author_id, painting_id, str(e)))
