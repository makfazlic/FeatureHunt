# scrape this website https://www.softwareadvice.com/categories/ everything in CategoriesResultComponent class
import scrapy


class SaCategoriesSpider(scrapy.Spider):
    name = "categories"
    start_urls = [
        'https://www.softwareadvice.com/categories/',
    ]

    def parse(self, response):
        titles = response.xpath('/html/body/div/div/div/section/main/section/section/h2/a/@href').getall()
        titles_text = response.xpath('/html/body/div/div/div/section/main/section/section/h2/a/text()').getall()
        print(len(titles))
        print(len(titles_text))
        for i, r in enumerate(titles):
            xpath = "/html/body/div/div/div/section/main/section/section["+str(i+1)+"]/ul/li/a/@href"
            xpath_text = "/html/body/div/div/div/section/main/section/section["+str(i+1)+"]/ul/li/a/text()"
            subtitles = response.xpath(xpath).getall()
            subtitles_text = response.xpath(xpath_text).getall()

            subtitles_obj = {}
            for j, s in enumerate(subtitles):
                subtitles_obj[subtitles_text[j]] = s
            yield {
                "category": {
                    titles_text[i]: titles[i],
                    "subcategory": subtitles_obj
                }
            }

        