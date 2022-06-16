import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider

class YmxSpider(RedisCrawlSpider):
    name = 'ymx'

    # 'https://www.amazon.cn/%E5%9B%BE%E4%B9%A6/b/ref=dp_bc_aui_C_1?ie=UTF8&node=658390051'
    allowed_domains = ['amazon.cn']
    # start_urls = ['https://www.amazon.cn/%E5%9B%BE%E4%B9%A6/b/ref=dp_bc_aui_C_1?ie=UTF8&node=658390051']
    redis_key = 'amazom'
    rules = (
        # 正好可以匹配大分类的url地址和小分类的url地址
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="a-section a-spacing-none"][1]/ul/li',)), follow=True),
        # 匹配图书的url地址
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="a-section a-spacing-medium"]//h2/..',)), callback='parse_book_detail'),
        # 列表页翻页
        # Rule(LinkExtractor(restrict_xpaths=('//div[@class="a-section a-spacing-large a-spacing-top-large a-text-center s-pagination-container"]',)),follow=True),

    )

    # def parse_item(self, response):
    #     item = {}
    #     #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
    #     #item['name'] = response.xpath('//div[@id="name"]').get()
    #     #item['description'] = response.xpath('//div[@id="description"]').get()
    #     return item

    def parse_book_detail(self,response):
        item = {}
        # 书名
        item['book_title'] = response.xpath('//span[@id="productTitle"]/text()').get()
        # 评论
        # item['book_comment'] = response.xpath("//span[@id='acrCustomerReviewText']/text()").getall()
        # 价格
        item['book_price'] = response.xpath('//span[@id="kindle-price"]/text()').get()
        # 书的作者
        item['book_name'] = response.xpath("//span[@class='author notFaded']/a/text()").getall()
        # 书的图片
        item['book_img'] = response.xpath("//div[@id='ebooks-img-canvas']/img/@src").get()
        print(item)

# 'https://www.amazon.cn/s?bbn=658394051&rh=n%3A658390051%2Cn%3A658394051%2Cn%3A658510051&dc&qid=1629437815&rnid=658394051&ref=lp_658394051_nr_n_2'
# 'https://www.amazon.cn/s?rh=n%3A658510051&fs=true&ref=lp_658510051_sar'





