import scrapy

class GaBaseSpider(scrapy.Spider):
    name = 'pe_categories'
    start_urls = [
        "https://www.peerspot.com/categories",
        ]

    def parse(self, response):
        urls_block = response.css(".container a::attr(href)").getall()
        yield {
            "urls" : urls_block
        }

    