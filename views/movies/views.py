from sanic import Sanic, json, response

from app_instance import app
from models import Movies


@app.get('/movies')
async def get_movies(request):
    artist = await Movies.find_one({"name": "A new rockstar!"})
    return response.json(artist.dump())


@app.post('/movies')
async def create_movies(request):
    artist = Movies(name="A new rockstar!", popularity=3, director="asdsadsa", genre=["abc", "xnd"], imdb_score=34)
    await artist.commit()
    return response.json(artist.dump())


@app.put('/movies')
async def update_movies(request):
    artist = await Movies.update({"name": "A new rockstar!"}, {"$set": {"director": "my_fav"}})
    return response.json(artist.dump())


@app.delete('/movies')
async def delete_movies(request):
    artist = await Movies.remove({"name": "A new rockstar!"})
    return response.json(artist.dump())
