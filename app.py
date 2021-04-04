from sanic import Sanic


app = Sanic("My Hello, world app")


from settings import db
from views.movies import views as movies
from views.users import views as users


if __name__ == '__main__':
    app.run()
