import asyncio
import uuid
import datetime
from urllib.parse import unquote
from sanic.views import HTTPMethodView
from sanic import response
from app_instance import app
from models import Movies


# @app.get('/movies')
# async def get_movies(request):
#     movie = await Movies.find_one({"name": "A new rockstar!"})
#     if movie:
#         return response.json(movie.dump())
#     else:
#         return response.json('{"result": "Movie not found by name"}')
#
#
# @app.post('/movies')
# async def create_movies(request):
#     # print(request.json)
#     # print(request.body)
#     # print(request.args)
#     # print(request.query_string)
#     # print(request.query_args)
#     movie = Movies(name="A new rockstar!", popularity=3, director="asdsadsa", genre=["abc", "xnd"], imdb_score=34)
#     await movie.commit()
#     return response.json(movie.dump())
#     # return response.json('{}')
#
#
# @app.put('/movies/<name>')
# async def update_movies(request, name):
#     from urllib.parse import unquote
#     name = unquote(name)
#     movie = await Movies.update({"name": name}, {"$set": {"director": "my_fav"}})
#     return response.json(movie.dump())
#
#
# @app.delete('/movies')
# async def delete_movies(request):
#     movie = await Movies.remove({"name": "A new rockstar!"})
#     return response.json(movie.dump())





class MoviesView(HTTPMethodView):

    async def get(self, request):
        if 'movie_id' in request.args:
            movie_id = unquote(request.args['movie_id'][0])
            movie = await Movies.find_one({"movie_id": movie_id}, {"_id": 0})
            movie = movie.to_mongo()
        elif 'limit' in request.args and 'page' in request.args:
            limit = int(request.args['limit'][0])
            page = int(request.args['page'][0])
            skip = page * limit - limit
            movie = Movies.collection.find({}).sort([("insert_datetime", -1)]).limit(limit).skip(skip)
            movie_list = []
            for r in await movie.to_list(length=limit):
                del r['_id']
                movie_list.append(r)

            movie = movie_list

        else:
            return response.json({"result": "Invalid data in request"})

        if movie:
            edit_mode = False
            if request.ctx.user and request.ctx.user['role'] == 'admin':
                edit_mode = True

            return response.json({"result": movie, "edit_mode": edit_mode})
        else:
            return response.json({"result": "Movie not found"})


    async def post(self, request):
        movies_data = request.json
        movies_data['movie_id'] = str(uuid.uuid4())
        movies_data['insert_datetime'] = str(datetime.datetime.now())
        movies_data['update_datetime'] = None
        movie = Movies(**movies_data)
        await movie.commit()
        return response.json({"result": "Successfully Saved Movie"})

    async def put(self, request):
        movie_id = unquote(request.args['movie_id'][0])
        movie = await Movies.find_one({"movie_id": movie_id})
        if movie:
            data = request.json
            data['update_datetime'] = str(datetime.datetime.now())
            movie.update(data)
            await movie.commit()
            return response.json({"result": "Successfully updated movie data"}, status=201)
        else:
            return response.json({"result": "Data not found to update"}, status=404)

    # async def patch(self, request):
    #     return text("I am patch method")

    async def delete(self, request):
        movie_id = unquote(request.args['movie_id'][0])
        movie = await Movies.find_one({"movie_id": movie_id})
        if movie:
            await movie.delete()
            return response.json({"result": "Successfully deleted data"}, status=200)
        else:
            return response.json({"result": "Data not found to delete"}, status=404)


app.add_route(MoviesView.as_view(), "/movies")



class GenreView(HTTPMethodView):

    async def get(self, request):
        genre = Movies.collection.distinct('genre', {})
        genre = await genre

        return response.json({"result": genre})


app.add_route(GenreView.as_view(), "/movies/genre")
