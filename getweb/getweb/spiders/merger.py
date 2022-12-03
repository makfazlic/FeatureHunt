import json

# open json
with open('categories.json') as f:
    categories = json.load(f)

with open('products.json') as f:
    products = json.load(f)

all_subs = []

for c in categories:
    # get key from c
    for url in c["subtitles"]:
        all_subs.append(url)

all_product_pages = {}
for url in all_subs:
    all_product_pages[url] = []
    for p in products:
        k = p.keys()
        v = p.values()
        if url == k:
            all_product_pages[url].append(v)

for pp in all_product_pages:
    print(all_product_pages[pp])
    break
