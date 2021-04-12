import os

from umongo import MotorAsyncIOInstance

mongo_db_config = {
    "MONGODB_DATABASE": "movies_db",
    "MONGODB_URI": "mongodb+srv://movies-db-user:PjONGrTy4MaCi4Ir@cluster0.uz3pi.mongodb.net/movies_db?retryWrites=true&w=majority",
    "MONGODB_CONNECT_OPTIONS": {
        "minPoolSize": 10,
        "maxPoolSize": 50
    },
    "LAZY_UMONGO": MotorAsyncIOInstance()
}
port = os.environ['PORT']
debug = False
