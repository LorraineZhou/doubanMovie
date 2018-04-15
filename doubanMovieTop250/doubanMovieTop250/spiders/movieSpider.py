#coding=utf-8
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from doubanMovie.items import DoubanmovieItem
import urllib


class doubanMovie(CrawlSpider):
    name='doubanMovie'
    start_urls=['https://movie.douban.com/top250?start=0&filter=']
    url = 'https://movie.douban.com'

    def parse(self, response):
        item = DoubanmovieItem()
        selector = Selector(response)
        articles = selector.xpath('// *[ @ id = "content"] / div / div[1]/ol/li')
        print(articles)

        for article in articles:
            name = article.xpath(' div / div[2] / div[1] / a / span[1] / text()').extract()
            rate = article.xpath(' div / div[2] / div[2] / div / span[2]/ text()').extract()
            commentNUM = article.xpath('div / div[2] / div[2] / div / span[4]/ text()').extract()
            comment = article.xpath(' div / div[2] / div[2] / p[2] / span/ text()').extract()
            item['name'] = name
            item['rate'] = rate
            item['commentNUM']=commentNUM
            item['comment']=comment

            yield item

        n=int(selector.xpath('//*[@id="content"]/div/div[1]/ol/li[1]/div/div[1]/em/text()').extract()[0])-1

        if n<=250 :
            n=n+25
            link='https://movie.douban.com/top250?start='+str(n)+'&filter='
            yield Request(link,callback=self.parse)

        # next_link = selector.xpath('//*[@id="list-container"]/div/button/@data-url').extract()
        #
        # if len(next_link)==1 :
        #     next_link = self.url+ str(next_link[0])
        #     print ("----"+next_link)
        #     yield Request(next_link,callback=self.parse)
