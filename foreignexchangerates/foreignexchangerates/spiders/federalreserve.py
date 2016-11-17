# -*- coding: utf-8 -*-
import scrapy

class FederalreserveSpider(scrapy.Spider):
    name = "federalreserve"
    # allowed_domains = ["federalreserve.gov"]
    start_urls = ['https://www.federalreserve.gov/releases/h10/hist/']

    def clean_data(self, txt):
        return txt.replace('  ', '')

    def parse(self, response):
        for href in response.xpath('//table[@class="statistics"]/tr/th/a/@href').extract():
            yield scrapy.Request(response.urljoin(href), callback=self.parse_rates)
            
    def parse_rates(self, response):
        for rate in response.xpath('//table[@class="statistics"]/tr'):
            yield {
                "country": response.xpath('//h3/text()').extract_first(),
                "date": self.clean_data(rate.xpath('th/text()').extract_first()),
                "rate": self.clean_data(rate.xpath('td/text()').extract_first())
                }


