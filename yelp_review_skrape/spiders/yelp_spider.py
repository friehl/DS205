import re
import scrapy
import os

from yelp_review_skrape.items import YPReview

def get_pages(self, response):
    reviews_per_page = 40
    total_reviews = int(response.xpath('//div[@class="rating-info clearfix"]//span[@itemprop="reviewCount"]/text()').extract()[0].strip().split()[0])
    pages = [scrapy.http.Request(url=response.url + '?start=' + \
        str(reviews_per_page*(n+1)), callback=self.parse) for n in range(total_reviews/reviews_per_page)]
    return pages

def get_urls():
    BASE_DIR = os.path.abspath('.')
    DATA_DIR = os.path.join(BASE_DIR, 'url_output')
    urls = []
    with open(os.path.join(DATA_DIR, 'urls.txt')) as f:
        for line in f:
            urls.append(line)
    return urls

class YelpSkraper(scrapy.Spider):
    name = 'yelp_review_skrape'
    start_urls = get_urls()

    def parse(self, response):
        requests = []
        base_path = response.xpath('//div[@class="review review--with-sidebar"]')

        for review in base_path:
            # Get fields that match Yelp Dataset review data
            item = YPReview()
            item['business_id'] = re.search(r'(?<=biz_id=)[^&]*', \
                response.xpath('//div[@class="price-category"]/a[@class="edit-category chiclet-link chiclet-link--with-text show-tooltip"]/@href')[0].extract()).group()
            item['user_id'] = re.search(r'(?<=userid=)[^&]*',
                review.xpath('.//li[@class="user-name"]/a/@href')[0].extract()).group()
            item['stars'] = review.xpath('.//meta[@itemprop="ratingValue"]/@content')[0].extract()
            item['date'] = review.xpath('.//meta[@itemprop="datePublished"]/@content')[0].extract()
            item['text'] = ' '.join(review.xpath('.//p[@itemprop="description"]/text()').extract())
            item['name'] = ' '.join(response.xpath('//h1[@class="biz-page-title embossed-text-white"]/text()').extract()).strip()
            item['id'] = response.url.split('/')[-1].split('?')[0]

            vote_cat = []
            vote_count = []
            votes_dict = {}
            voting_path = review.xpath('.//li[@class="voting-stat inline-block"]')
            for i in voting_path:
                vote_cat.append(i.xpath('.//span[@class="vote-type"]/text()').extract()[0])
                vt = i.xpath('.//span[@class="count"]/text()').extract()
                if len(vt) == 0:
                    vt = [0]
                vote_count.append(int(vt[0]))
            for j in range(len(vote_cat)):
                votes_dict[vote_cat[j]] = vote_count[j]
            item['votes'] = votes_dict
            item['type'] = 'Review'

            yield item

        # Paginate through additional reviews
        if response.url.find('?start=') == -1:
            requests += get_pages(self, response)
            print requests
            for request in requests:
                yield request
