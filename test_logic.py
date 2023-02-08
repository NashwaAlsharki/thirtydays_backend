import json

f = open('exercises.json')
data = json.load(f)
base_url = 'https://raw.githubusercontent.com/everkinetic/data/main/src/images-web/'


@app.post('/upload')
async def upload():
    to_add = []
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

        exercise = jsonable_encoder(exercise)
        to_add.append(exercise)

    added = await exercises_db.insert_many(to_add)
    return {"message": f"added all {len(to_add)} exercises"}