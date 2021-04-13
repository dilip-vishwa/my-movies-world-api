import logging
import os
logging.getLogger('sanic_cors').level = logging.DEBUG
from sanic import Sanic, response
from sanic_cors import CORS
import jwt

if 'ENV' in os.environ and os.environ['ENV'] == "production":
    from config import production as settings
else:
    from config import development as settings

app = Sanic("My Hello, world app")

CORS(app)


async def extract_user_from_request(request):
    user_info = {}
    if request.token and request.token != 'null':
        user_info = jwt.decode(request.token, "secret", algorithms=["HS256"])
        role = user_info['role']
        # TODO: extract jwt and find if the user is authenticated and is of given role
    else:
        role = 'anonymous'

    # if role == "admin" and request.uri_template in ['/movies', '/movies/<name>', '/users', '/movies/genre'] and request.method in ['GET', 'POST', 'PUT', 'DELETE']:
    #     pass
    # elif role == "anonymous" and request.uri_template in ['/movies'] and request.method in ['GET']:
    #     pass
    # elif role == "anonymous" and request.uri_template in ['/users'] and request.method in ['POST']:
    #     pass
    # else:
    #     return "Unauthorized"

    return user_info

# @app.listener('before_server_start')
# async def setup_db(app, loop):
#     # app.db = await db_setup()
#     print('before_server_start')
#
# @app.listener('after_server_start')
# async def notify_server_started(app, loop):
#     print('Server successfully started!')
#
# @app.listener('before_server_stop')
# async def notify_server_stopping(app, loop):
#     print('Server shutting down!')
#
# @app.listener('after_server_stop')
# async def close_db(app, loop):
#     # await app.db.close()
#     print('after_server_stop')


@app.middleware('request')
async def extract_user(request):
    data = await extract_user_from_request(request)
    if data == 'Unauthorized':
        return response.json({"result": "Unauthorized"}, status=403)
    else:
        request.ctx.user = data


# @app.middleware('response')
# async def custom_banner(request, response):
#     response.headers["Server"] = "Fake-Server"
#     print("Faking response")


from settings import db
from views.movies import views as movies
from views.users import views as users


if __name__ == '__main__':
    app.run(debug=settings.debug, port=settings.port)
