# We need to scrape the following information from the profile page:
# 1. Name
# 2. Logo and images
# 3. Description
# 4. Pricing
# 5. Reviews
#    5.1. Reviewer Name
#    5.2. Reviewer Info
#    5.3. Reviewer Image
#    5.4. General Review
#    5.5. Pros
#    5.6. Cons
# 6. Overall Raiting
# 7. Secondary Raiting
#    7.1. Ease-of-Use
#    7.2. Customer Support
#    7.3. Value for money
#    7.4. Functionality
# 8. Link to the Company Website
# 9. Link to the Company Profile

pricing = {
    'general': 'None',
    'starting_price': 'None',
    'free_trial': 'None',
    'free_version': 'None',
}

# review = {
#     'reviewer_name': 'None',
#     'reviewer_info': {
#         'company_size': 'None',
#         'industry': 'None',
#         'time_used': 'None'
#     },
#     #'reviewer_image': '',
#     'general_review_title': 'None',
#     'general_review': 'None',
#     'pros': 'None',
#     'cons': 'None'
# }

review = {
    'reviewer_name': 'None',
    'reviewer_info': [],
    #'reviewer_image': '',
    'general_review_title': 'None',
    'general_review': 'None',
    'pros': 'None',
    'cons': 'None'
}


profile = {
    'name': '',
    'logo': '',
    'images': [],
    'description': '',
    'pricing': [],
    'reviews': [],
    'overall_raiting': '',
    'secondary_raiting': {
        'ease_of_use': '',
        'customer_support': '',
        'value_for_money': '',
        'functionality': ''
    },
    'website': '',
    'profile_link': ''
}

import scrapy
import json
from bs4 import BeautifulSoup

class SaProfileSpider(scrapy.Spider):
    name = "profile"

    def start_requests(self):
        with open('merged.json', 'r') as f:
            data = json.load(f)
        for category in data:
            for subcategory in category["category"]["subcategory"]:
                if subcategory == "Accounting Software for Consultants":
                    url_list = category["category"]["subcategory"][subcategory]
                    for url in url_list:
                        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        
        # 1. Name
        name = response.xpath('/html/body/div/div/div/section/main/div[2]/main/section/div[1]/div/section/div[1]/div[2]/h1/text()').get()
        
        # 2. Logo and images
        logo = response.xpath('/html/body/div/div/div/section/main/div[2]/main/section/div[1]/div/section/div[1]/div[1]/img/@src').get()
        mainimage = response.xpath('/html/body/div/div/div/section/main/div[2]/main/div/div/div/div/div[3]/section/div[1]/img/@src').get()
        subimages = response.xpath('/html/body/div/div/div/section/main/div[2]/main/div/div/div/div/div[3]/section/div[2]/section/div/div[5]/div').get()
        try:
            soup = BeautifulSoup(subimages, 'html.parser')
            subimages = [image["src"] for image in soup.find_all('img')]
            images = [mainimage] + subimages
        except:
            images = [mainimage]
        
        # 3. Description
        description = response.xpath('/html/body/div/div/div/section/main/div[2]/main/div/div/div/div/div[1]/div/div[1]/div[1]/text()').get()
        description = description.replace('\r', '\n')
        description = description.split('\n')
        new_description = ""
        for i in range(len(description)):
            if "..." in description[i]:
                break
            new_description += description[i] + " "
        new_description = " ".join(new_description.split())
        description = new_description

        # 4. Pricing
        # make a copy of an object
        pricing_copy = pricing.copy()
        general = response.xpath('/html/body/div/div/div/section/main/div[2]/main/div/div/div/div/div[1]/div/div[2]/div/div/div/div/p/text()').get()
        if general:
            pricing_copy['general'] = general
        starting_price = response.css('#pricing > div > div > div > div > div.pricing-details__price > p.small.bold::text').getall()
        if starting_price:
            # for i in range(len(starting_price)):
            #     pricing_copy['starting_price'] += starting_price[i]
            pricing_copy['starting_price'] = "".join(starting_price).split("\u00a0")[0] + " " + "".join(starting_price).split("\u00a0")[1]
        free_trial = response.css('#pricing > div > div > div > div > div.pricing-details__freetrial > p.small.bold::text').get()
        if free_trial:
            pricing_copy['free_trial'] = free_trial
        free_version = response.css('#pricing > div > div > div > div > div.pricing-details__freeversion > p.small.bold::text').get()
        if free_version:
            pricing_copy['free_version'] = free_version

        # 5. Reviews
        array_of_reviews = []
        reviews = response.xpath('/html/body/div/div/div/section/main/div[2]/main/div/div/section[1]/section/div[2]/div/div/div/div/div[1]/div/div[2]/div').getall()
        for i, r in enumerate(reviews):
            review_copy = review.copy()
            r_soup = BeautifulSoup(r, 'html.parser')
            review_copy['reviewer_info'] = []
            try:
                rev_person_block = r_soup.find('div', id='review-person')
                review_copy['reviewer_name'] = rev_person_block.find('div', class_='review-profile-user').text
            except:
                review_copy['reviewer_name'] =  "Anonymous"
        
            try:
                rev_person_block = r_soup.find('div', id='review-person')
                review_copy['reviewer_info'].append(rev_person_block.find('div', class_='review-company').text)
            except:
                review_copy['reviewer_info'].append("Unknown")
            try:
                rev_person_block = r_soup.find('div', id='review-person')
                review_copy['reviewer_info'].append(rev_person_block.find('div', class_='review-gdm-industry').text)
            except:
                review_copy['reviewer_info'].append("Unknown")
            try:
                rev_person_block = r_soup.find('div', id='review-person')
                review_copy['reviewer_info'].append(rev_person_block.find('div', class_='review-profile-time-used').text)
            except:
                review_copy['reviewer_info'].append( "Unknown")
            try:
                rev_block = r_soup.find('div', class_='review-copy-container')
                review_copy['general_review_title'] = rev_block.find('p', class_='review-copy-header').text
                review_copy['general_review'] =rev_block.find('p', class_='review-copy-summary').text
            except:
                review_copy['general_review_title'] = "None"
                review_copy['general_review'] = "None"
            try:
                rev_block = r_soup.find('div', class_='review-copy-container')
                ui = rev_block.find_all('p')
                ui = [i.text for i in ui]
                review_copy['pros'] = "None"
                review_copy['cons'] = "None"
                if "Pros" in ui:
                    review_copy['pros'] = ui[ui.index("Pros") + 1]
                if "Cons" in ui:
                    review_copy['cons'] = ui[ui.index("Cons") + 1]
            except:
                ui = "None"
                review_copy['pros'] = "None"
                review_copy['cons'] = "None"
            
            review_copy["index"] = i

            array_of_reviews.append(review_copy)


        
        
        # 6. Overall Raiting
        overall_raiting = response.xpath('//*[@id="reviews"]/section/div[1]/div/div/div[1]/h1/text()').get()
        
        # 7. Secondary Raiting
        #    7.1. Ease-of-Use
        ease_of_use = response.xpath('//*[@id="reviews"]/section/div[1]/div/div/div[3]/div[1]/p[2]/text()').get()
        #    7.2. Customer Support
        customer_support = response.xpath('//*[@id="reviews"]/section/div[1]/div/div/div[3]/div[2]/p[2]/text()').get()
        #    7.3. Value for money
        value_for_money = response.xpath('//*[@id="reviews"]/section/div[1]/div/div/div[3]/div[3]/p[2]/text()').get()
        #    7.4. Functionality
        functionality = response.xpath('//*[@id="reviews"]/section/div[1]/div/div/div[3]/div[4]/p[2]/text()').get()

        # 8. Website
        website = response.xpath('/html/body/div/div/div/section/main/div[2]/main/section/div[1]/div/section/div[2]/section/section/a/@data-href').get()
        
        # 9. Link to the Company Profile
        profile = response.url
        
        yield {
            'profile' : profile,
            'name': name,
            'logo': logo,
            'images': images,
            'description': description,
            'pricing': pricing_copy,
            'reviews': array_of_reviews,
            'overall_raiting': overall_raiting,
            'secondary_raiting': {
                 'ease_of_use': ease_of_use,
                 'customer_support': customer_support,
                 'value_for_money': value_for_money,
                 'functionality': functionality
             },
            'website': website,
        }