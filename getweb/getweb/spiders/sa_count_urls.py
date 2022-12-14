import json

with open('merged.json') as f:
    data = json.load(f)

count = 0
for c in data:
    for sc in c['category']['subcategory']:
        # write to file 
        count += len(c['category']['subcategory'][sc])

print(count)
