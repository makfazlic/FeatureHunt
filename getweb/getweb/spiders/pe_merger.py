import json

all_urls = {
    "companies": []
    }
with open('pe_companies.json') as f:
    categories = json.load(f)
    for category in categories:
        for url in category["url"]:
            all_urls["companies"].append(url)

with open('pe_companies_merged.json', 'w') as f:
    json.dump(all_urls, f)