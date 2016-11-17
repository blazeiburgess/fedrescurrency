# -*- coding: utf-8 -*-
import scrapy


class FederalreserveSpider(scrapy.Spider):
    name = "federalreserve"
    allowed_domains = ["federalreserve.gov"]
    start_urls = ['http://federalreserve.gov/']

    def parse(self, response):
        pass
