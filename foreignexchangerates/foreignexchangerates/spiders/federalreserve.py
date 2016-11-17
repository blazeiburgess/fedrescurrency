# -*- coding: utf-8 -*-
import scrapy

class FederalreserveSpider(scrapy.Spider):
    name = "federalreserve"
    allowed_domains = ["federalreserve.gov"]
    start_urls = ['http://federalreserve.gov/']

    def parse(self, response):
        urls = list(map(response.urljoin, response.xpath('//table[@class="statistics"]/tbody/tr/th/a/@href')))
        if len(urls) == 0:
            for rate in response.xpath('//table[@class="statistics"]/tr'):
                yield {
                    "country": response.xpath('//h3/text()'),
                    "date": rate.xpath('//th/text()'),
                    "rate": rate.xpath('//td/text()')
                }
        else:
            for url in urls:
                yield scrapy.Request(url, callback=self.parse)
