from urllib.parse import unquote
from sanic.views import HTTPMethodView
from sanic import response
from app_instance import app
from models import Movies, Users
import jwt

class UsersView(HTTPMethodView):

    async def post(self, request):
        body = eval(request.body)
        if 'username' in body:
            password = body['password']
            username = body['username']

            user = await Users.find_one({"username": username, "password": password})

        if user:

            encoded_jwt = jwt.encode({"username": username, "role": user.role, "role": user['role']}, "secret", algorithm="HS256")
            # print(encoded_jwt)
            # eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzb21lIjoicGF5bG9hZCJ9.Joh1R2dYzkRvDkqv3sygm5YyK8Gi4ShZqbhK2gxcs2U
            # {'some': 'payload'}

            custom_response = response.json({"result": "Success", "auth_token": encoded_jwt}, status=200)
            # custom_response.cookies['auth_token'] = encoded_jwt
            # custom_response.cookies["auth_token"]["httponly"] = True
            return custom_response
        else:
            return response.json({"result": "Username or Password is incorrect"}, status=401)

    # async def post(self, request):
    #     movie = Movies(**request.json)
    #     await movie.commit()
    #     return response.json(movie.dump())

    # async def put(self, request):
    #     name = unquote(request.args['name'][0])
    #     movie = await Movies.find_one({"name": name})
    #     if movie:
    #         movie.update(request.json)
    #         await movie.commit()
    #         return response.json({"result": "Successfully deleted data"}, status=201)
    #     else:
    #         return response.json({"result": "Data not found to update"}, status=404)

    # async def patch(self, request):
    #     return text("I am patch method")

    # async def delete(self, request):
    #     name = unquote(request.args['director'][0])
    #     movie = await Movies.find_one({"director": name})
    #     if movie:
    #         await movie.delete()
    #         return response.json({"result": "Successfully deleted data"}, status=204)
    #     else:
    #         return response.json({"result": "Data not found to delete"}, status=404)


app.add_route(UsersView.as_view(), "/users")
