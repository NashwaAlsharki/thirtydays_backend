import json
f = open('exercises.json')
data = json.load(f)

# understand exercise data
def understand():
    counts = {'title': 0, 'primer': 0, 'style': 0, 'primary': 0, 'secondary': 0, 'equipment': 0, 'steps': 0, 'tips': 0, 'img': 0, 'img_count': {0: 0, 1: 0, 2:0, 3:0, 4:0}}

    for item in data:
        for key in counts:
            if key in item:
                counts[key] += 1
                if key == 'img':
                    counts['img_count'][len(item[key])] += 1
    
    print(counts)

# create excercise model to add to database
def upload():
    to_add = []
    base_url = 'https://raw.githubusercontent.com/everkinetic/data/main/src/images-web/'
    for item in data:
        d ={ 'title': '', 'primer': '', 'style': '', 'primary': '', 'secondary': [], 'equipment': [], 'steps': [], 'tips': [], 'img': []}
        for key in d:
            if key in item:
                d[key] = item[key]

        image_urls = []
        for img in d['img']:
            name = img.split('web/')[1]
            image_urls.append(base_url+name)

        exercise = ExerciseModel(
            title=d['title'],
            primer=d['primer'],
            style=d['style'],
            primary=d['primary'],
            secondary=d['secondary'],
            equipment=d['equipment'],
            steps=d['steps'],
            tips=d['tips'],
            image_urls=image_urls
        )
        to_add.append(exercise)

    print(f'Ready to upload all {len(to_add)} exercises')

# see what muscle groups are in the data
def muscles():
    muscles = set()
    for item in data:
        if 'primary' in item:
            muscles.add(item['primary'])
        if 'secondary' in item:
            for muscle in item['secondary']:
                muscles.add(muscle)
    print(muscles)

muscles()


