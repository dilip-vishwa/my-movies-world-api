from sanic_mongodb_ext import MongoDbExtension
from umongo import MotorAsyncIOInstance
from app_instance import app


app.config.update({
    "MONGODB_DATABASE": "movies_db", # Make ensure that the `app` database is really exists
    "MONGODB_URI": "mongodb://localhost:27017",
    # "MONGODB_URI": "mongodb+srv://movies-db-user:<password>@cluster0.uz3pi.mongodb.net/movies_db?retryWrites=true&w=majority",
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
