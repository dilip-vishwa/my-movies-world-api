import asyncio
import re
import uuid
import datetime
from urllib.parse import unquote
from sanic.views import HTTPMethodView
from sanic import response
from app_instance import app
from models import Movies


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
            query = {}
            if 'movie_name' in request.args:
                movie_name = unquote(request.args['movie_name'][0])
                query = {"name": re.compile(movie_name, re.IGNORECASE)}

            movie = Movies.collection.find(query).sort([("insert_datetime", -1)]).limit(limit).skip(skip)
            movie_list = []
            for r in await movie.to_list(length=limit):
                del r['_id']
                movie_list.append(r)

            movie = movie_list

        else:
            return response.json({"result": "Invalid data in request"})

        if movie:
            print(movie)
            edit_mode = False
            if request.ctx.user and request.ctx.user['role'] == 'admin':
                edit_mode = True

            return response.json({"result": movie, "edit_mode": edit_mode}, status=200)
        else:
            return response.json({"result": [], "message": "Movie not found"}, status=200)


    async def post(self, request):
        movies_data = request.json
        movie_id = str(uuid.uuid4())
        movies_data['movie_id'] = movie_id
        movies_data['insert_datetime'] = str(datetime.datetime.now())
        movies_data['update_datetime'] = None
        movie = Movies(**movies_data)
        await movie.commit()
        return response.json({"result": "Successfully Saved Movie", "movie_id": movie_id}, status=201)


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
