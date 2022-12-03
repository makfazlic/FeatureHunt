# scrape this website https://www.softwareadvice.com/categories/ everything in CategoriesResultComponent class
import scrapy
import json

class SaCompaniesSpider(scrapy.Spider):
    name = "companies"

    def start_requests(self):
        with open('categories.json', 'r') as f:
            data = json.load(f)
        for category in data:
            for url in category["subtitles"]:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # all the companies in the tab
        links = response.css("div.ProductCardComponent > a:nth-child(1)::attr(href)").getall()
        yield {
            response.url: links
        }
        

        