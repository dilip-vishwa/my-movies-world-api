import json

import requests

movie_id = ""

def test_post_movies():
    global movie_id
    movie_data = {
        "name": "Test movie",
        "popularity": 3,
        "director": "asdsadsa",
        "genre": [
            "abc",
            "xnd"
        ],
        "imdb_score": 34
    }
    response = requests.post("http://localhost:8000/movies/", data=json.dumps(movie_data))
    assert response.status_code == 201
    response_body = response.json()
    # assert response_body["result"] == "No data exists for US zip code 90210"
    movie_id = response_body['movie_id']
    print(response_body['result'])
    assert True


def test_get_movies():
    response = requests.get(f"http://localhost:8000/movies/?movie_id={movie_id}")
    assert response.status_code == 200
    response_body = response.json()
    assert response_body['result']['name'] == "Test movie" and response_body['result']['imdb_score'] == 34


def test_put_movies():
    movie_data = {"imdb_score": 84}
    response = requests.put(f"http://localhost:8000/movies/?movies={movie_id}", data=json.dumps(movie_data))
    assert response.status_code == 200
    response_body = response.json()
    print(response_body['result'])
    assert True

def test_get_movies_on_change():
    response = requests.get(f"http://localhost:8000/movies/?movie_id={movie_id}")
    assert response.status_code == 200
    response_body = response.json()
    assert response_body['result']['imdb_score'] == 84

#
# def test_delete_movies():
#     response = requests.delete("http://localhost:8000/movies/")
#     assert response.status_code == 200
#     response_body = response.json()
#     # assert response_body["result"] == "No data exists for US zip code 90210"
#     print(response_body['result'])
#     assert True
