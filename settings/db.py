import os

from sanic_mongodb_ext import MongoDbExtension
from umongo import MotorAsyncIOInstance
from app_instance import app

if 'ENV' in os.environ and os.environ['ENV'] == "production":
    from config import production as settings
else:
    from config import development as settings

app.config.update(settings.mongo_db_config)

# uMongo client is available as `app.mongodb` or `app.extensions['mongodb']`.
# The lazy client will be available as `app.lazy_mongodb` only when the database was specified,
# and which is a great choice for the structured projects.
MongoDbExtension(app)
