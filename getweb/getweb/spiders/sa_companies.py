# scrape this website https://www.softwareadvice.com/categories/ everything in CategoriesResultComponent class
import scrapy
import json

class SaCompaniesSpider(scrapy.Spider):
    name = "sa_companies"

    def start_requests(self):
        with open('sa_categories.json', 'r') as f:
            data = json.load(f)
        for category in data:
            for subcategory in category["category"]["subcategory"]:
                url = category["category"]["subcategory"][subcategory]
                yield scrapy.Request(url=url, callback=self.parse)
                

    def parse(self, response):
        # all the companies in the tab
        links = response.css("div.ProductCardComponent > a:nth-child(1)::attr(href)").getall()
        yield {
            response.url: links
        }
        

        