from sanic import Sanic
from sanic.response import json
from sanic_mongodb_ext import MongoDbExtension
from umongo import Instance, Document, MotorAsyncIOInstance
from umongo.fields import StringField, IntegerField, ListField


app = Sanic("My Hello, world app")

app.config.update({
    "MONGODB_DATABASE": "app", # Make ensure that the `app` database is really exists
    "MONGODB_URI": "mongodb://localhost:27017",
    "MONGODB_CONNECT_OPTIONS": {
        "minPoolSize": 10,
        "maxPoolSize": 50
    },
    "LAZY_UMONGO": MotorAsyncIOInstance()
})
# uMongo client is available as `app.mongodb` or `app.extensions['mongodb']`.
# The lazy client will be available as `app.lazy_mongodb` only when the database was specified,
# and which is a great choice for the structured projects.
MongoDbExtension(app)


# Describe the model
@app.lazy_umongo.register
class Movies(Document):
    name = StringField(required=True, allow_none=False)
    popularity = IntegerField()
    director = StringField(required=True, allow_none=False)
    genre = ListField()
    imdb_score = IntegerField()


@app.get('/movies')
async def get_movies(request):
    return json({'hello': 'world'})


@app.post('/movies')
async def create_movies(request):
    return json({'hello': 'world'})


@app.put('/movies')
async def update_movies(request):
    return json({'hello': 'world'})


@app.delete('/movies')
async def delete_movies(request):
    return json({'hello': 'world'})

if __name__ == '__main__':
    app.run()
