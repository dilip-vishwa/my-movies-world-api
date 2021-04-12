############## Code to do some changes in movies data ############################

# movie = Movies.collection.find({}, {"_id": 0})
# movie_list = []
# for r in await movie.to_list(length=1000):
#     movie_list.append(r)
#
# for m in movie_list:
#     movie = await Movies.find_one({"name": m['name']})
#     if movie:
#         # movie.update({'movie_id': str(uuid.uuid4())})
#         movie.update({'insert_datetime': str(datetime.datetime.now()), 'update_datetime': None})
#         await movie.commit()
#         await asyncio.sleep(0.5)

####################################################################################
