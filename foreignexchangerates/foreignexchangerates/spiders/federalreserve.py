# -*- coding: utf-8 -*-
import scrapy

class FederalreserveSpider(scrapy.Spider):
    name = "federalreserve"
    allowed_domains = ["federalreserve.gov"]
    start_urls = ['http://federalreserve.gov/']

    def parse(self, response):
        for url in response.xpath('//table[@class="statistics"]/tbody/tr/th/a/@href'):
            yield scrapy.Request(response.urljoin(href), callback=self.parse_rates)
            
    def parse_rates(self, response):
        for rate in response.xpath('//table[@class="statistics"]/tr'):
            yield {
                "country": response.xpath('//h3/text()'),
                "date": rate.xpath('//th/text()'),
                "rate": rate.xpath('//td/text()')
                }


