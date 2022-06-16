import scrapy
from scrapy_redis.spiders import RedisSpider
from copy import deepcopy
from ..items import BookItem
import urllib
class DangSpider(RedisSpider):
    name = 'dang'
    allowed_domains = ['dangdang.com']
    # start_urls = ['https://book.dangdang.com/']
    redis_key = "dang"  # 键
    def parse(self, response):
        # 大分类分组
        div_list = response.xpath("//div[@class='con flq_body']/div")
        for div in div_list:
            item = {}
            item['b_cate'] = div.xpath("./dl/dt//text()").getall()
            # 切割空字符串换行符
            item['b_cate'] = [i.strip() for i in item['b_cate'] if len(i.strip())>0]
            # 中间分类分组
            dl_list = div.xpath("./div//dl[@class='inner_dl']")
            for dl in dl_list:
                # 注意  因为这里获取的文本内容标签不一样所以直接//text()有换行符空格字符串
                item['m_cate'] = dl.xpath("./dt//text()").getall()
                # # 切割空字符串换行符  因为取的是第一个 索引就为0
                item['m_cate'] = [i.strip() for i in item['m_cate'] if len(i.strip())>0][0]
                # 小分类分组
                a_list = dl.xpath("./dd/a")
                for a in a_list:
                    # 里面的响应相对应
                    item["s_href"] = a.xpath("./@href").get()
                    item["s_cate"] = a.xpath("./text()").get()
                    if item["s_href"] is not None:
                        yield scrapy.Request(
                            item["s_href"],
                            callback=self.parse_book_list,
                            meta={'item':deepcopy(item)}
                        )

    def parse_book_list(self,response):
        item = response.meta['item']
        li_list = response.xpath("//ul[@class='bigimg']/li")
        for li in li_list:
            item["book_img"] = li.xpath("./a[@class='pic']/img/@src").get()
            if item["book_img"] == "images/model/guan/url_none.png":
                item["book_img"] = li.xpath("./a[@class='pic']/img/@data-original").get()
            item["book_name"] = li.xpath("./p[@class='name']/a/@title").get()
            item["book_desc"] = li.xpath("./p[@class='detail']/text()").get()
            print(item)

        # 下一页
        next_url = response.xpath("//li[@class='next']/a/@href").get()
        if next_url is not None:
            next_url = urllib.parse.urljoin(response.url,next_url)
            yield scrapy.Request(
                next_url,
                callback=self.parse_book_list,
                meta={'item':item}
            )


