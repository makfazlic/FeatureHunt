# scrape this website https://www.softwareadvice.com/categories/ everything in CategoriesResultComponent class
import scrapy


class SaCategoriesSpider(scrapy.Spider):
    name = "categories"
    start_urls = [
        'https://www.softwareadvice.com/categories/',
    ]

    def parse(self, response):
        titles = response.xpath('/html/body/div/div/div/section/main/section/section/h2/a/text()').getall()
        for i, r in enumerate(titles):
            xpath = "/html/body/div/div/div/section/main/section/section["+str(i+1)+"]/ul/li/a/text()"
            subtitles = response.xpath(xpath).getall()
            yield {
                'title': r,
                'subtitles': subtitles
            }

        