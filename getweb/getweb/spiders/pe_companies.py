import scrapy
import json

class GaCompanieSpider(scrapy.Spider):
    name = "pe_companies"


    def start_requests(self):
        with open('pe_categories.json', 'r') as f:
            data = json.load(f)[0]
        data = data["urls"]
        for url in data:
            url = "https://www.peerspot.com" + url
            yield scrapy.Request(url=url, callback=self.parse)
            

    def parse(self, response):
        # all the companies in the tab
        profile_links = response.css("li.top_20_product_line > div:nth-child(3) > div:nth-child(1) a::attr(href)").getall()
        profile_links = ["https://www.peerspot.com" + link for link in profile_links]
        yield {
            "url": profile_links
        }

