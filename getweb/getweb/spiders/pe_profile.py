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

class PeProfileSpider(scrapy.Spider):
    name = 'pe_profile'
    
    
    def start_requests(self):
        with open('pe_companies_merged.json') as f:
            data = json.load(f)
        companies = data['companies']
        for company in companies:
            scrapy.Request(url=company, callback=self.parse)

    def parse(self, response):
        
