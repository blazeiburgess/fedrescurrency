# -*- coding: utf-8 -*-
import scrapy

class FederalreserveSpider(scrapy.Spider):
    name = "federalreserve"
    allowed_domains = ["federalreserve.gov"]
    start_urls = ['https://www.federalreserve.gov/releases/h10/hist/']

    def clean_country(self, txt):
        return txt.replace("Historical Rates for the ", "")

    # main `parse` method pulls in urls where data is stored
    def parse(self, response):
        hrefs = response.xpath('//table[@class="statistics"]/tr/th/a/@href').extract()

        # handles if the <th> country column is switched/made into a <td> 
        if len(hrefs) == 0:
            hrefs = response.xpath('//table[@class="statistics"]/tr/td/a/@href').extract()
            
        # takes pulled urls and uses them to yield results from the `parse_rates` method
        for href in hrefs:
            yield scrapy.Request(response.urljoin(href), callback=self.parse_rates)
            
    # parser that specifically handles the desired data
    def parse_rates(self, response):
        for rate in response.xpath('//table[@class="statistics"]/tr'):
            yield {
                "currency": self.clean_country(response.xpath('//h3/text()').extract_first().strip()),
                "date": rate.xpath('th/text()').extract_first().strip(),
                "rate": rate.xpath('td/text()').extract_first().strip()
                }


