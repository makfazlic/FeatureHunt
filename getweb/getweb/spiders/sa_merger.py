# import json

# # open json
# categories = []
# # with open('categories_v2.json') as f:
# #     categories = json.load(f)

# companies = []
# # with open('companies_v2.json') as f:
# #     companies = json.load(f)

# # merge where subcategory url is equal to company url
# my_categories = categories
# for i, category in enumerate(categories):
#     for subcategory in category["category"]["subcategory"]:
#         for company in companies:
#             #print(category["category"]["subcategory"][subcategory], )
#             if category["category"]["subcategory"][subcategory] == list(company.keys())[0]:
#                 my_categories[i]["category"]["subcategory"][subcategory] = list(company.values())[0]


# # save merged json    
# with open('merged.json', 'w') as f:
#     json.dump(my_categories, f)
