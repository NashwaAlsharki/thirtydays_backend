import json
f = open('exercises.json')
data = json.load(f)
base_url = 'https://raw.githubusercontent.com/everkinetic/data/main/src/images-web/'

for item in data[0:5]:
    item['img_link'] = []
    for img in item['img']:
        name = img.split('web/')[1]
        item['img_link'].append(base_url+name)
