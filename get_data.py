import requests
import os
from tmdb import URLMaker


# POSTER_ROOT = 'https://www.themoviedb.org/t/p/original'
# my_url = URLMaker(TMDB_API_KEY)
# for i in range(1,100):
#     target = my_url.get_url(page=i, language='ko-KR')
#     res = requests.get(target)
#     movies = res.json().get('results')
#     for movie in movies:
#         if movie.get('vote_average') >= 8 and movie.get('vote_count') >= 100:
#             add_movie = dict()
#             add_movie['title'] = movie.get('title')
#             add_movie['overview'] = movie.get('overview')
#             add_movie['release_date'] = movie.get('release_date')
#             add_movie['poster_path'] = POSTER_ROOT+movie.get('poster_path')
#             print(add_movie)