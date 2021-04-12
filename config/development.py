from umongo import MotorAsyncIOInstance

mongo_db_config = {
    "MONGODB_DATABASE": "movies_db",
    "MONGODB_URI": "mongodb://localhost:27017",
    "MONGODB_CONNECT_OPTIONS": {
        "minPoolSize": 10,
        "maxPoolSize": 50
    },
    "LAZY_UMONGO": MotorAsyncIOInstance()
}
port = 8000
debug = True
