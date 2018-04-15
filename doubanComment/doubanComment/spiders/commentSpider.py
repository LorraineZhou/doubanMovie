#coding=utf-8
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from doubanComment.items import DoubancommentItem
import urllib


class doubanComment(CrawlSpider):
    name='doubanComment'
    start_urls=['http://xueshu.baidu.com/s?wd=%E7%94%B5%E5%8C%96%E6%95%99%E8%82%B2%E7%A0%94%E7%A9%B6&pn=0&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8&usm=1&tag_filter=%20%20%20jnls%3A%28%E3%80%8A%E7%94%B5%E5%8C%96%E6%95%99%E8%82%B2%E7%A0%94%E7%A9%B6%E3%80%8B%29&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D&bcp=2&sc_hit=1']
    url = 'http://xueshu.baidu.com'

    def parse(self, response):
        item = DoubancommentItem()
        selector = Selector(response)
        articles = selector.xpath('// *[ @ id = "comments"]/div')

        for i in range(20,2000,20):
            link='https://movie.douban.com/subject/3072086/comments?start='+str(i)+'&limit=20&sort=new_score&status=P&percent_type='
            for article in articles:
                rate = article.xpath('div[2] / h3 / span[2] / span[2]/ @title').extract()
                comment = article.xpath(' div[2] / p / text()').extract()
         #       item['rate'] = rate
                item['comment'] = comment

                yield item
            yield Request(link,callback=self.parse)

        # next_link = selector.xpath('//*[@id="list-container"]/div/button/@data-url').extract()
        #
        # if len(next_link)==1 :
        #     next_link = self.url+ str(next_link[0])
        #     print ("----"+next_link)
        #     yield Request(next_link,callback=self.parse)
