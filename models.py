from app_instance import app
from umongo import Document
from umongo.fields import StringField, IntegerField, ListField

@app.lazy_umongo.register
class Movies(Document):
    name = StringField(required=True, allow_none=False)
    popularity = IntegerField()
    director = StringField(required=True, allow_none=False)
    genre = ListField(StringField(required=True, allow_none=False))
    imdb_score = IntegerField()


@app.lazy_umongo.register
class Users(Document):
    username = StringField(required=True, allow_none=False)
    password = StringField(required=True, allow_none=False)
    role = StringField(required=True, allow_none=False)
