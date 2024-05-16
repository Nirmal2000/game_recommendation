import requests
import pickle
from fuzzywuzzy import process
from datetime import datetime

class IGDB:
    def __init__(self, cid, bearer):
        self.cid = cid
        self.bearer = bearer
        self.games_url = 'https://api.igdb.com/v4/games'
        self.cover_url = 'https://api.igdb.com/v4/covers'
        try:
            self.cache = pickle.load(open('./files/igdb_cache.pkl','rb'))
        except:
            self.cache = {}
        
        self.headers = {
            'Client-ID': cid,
            'Authorization': f'Bearer {bearer}',
            'Accept': 'application/json'
        }
        
    def _request_(self, url, data):
        from app import mongo
        mongo_response = mongo.db.api_cache.find_one({'url': url, 'data': data, 'request_type': 'POST'})
        if mongo_response:
            return mongo_response['response']
        while 1:
            response = requests.post(url, headers=self.headers, data=data)  
            if response.status_code == 200:
                mongo.db.api_cache.insert_one({'url': url, 'data': data, \
                                               'request_type': 'POST', 'response': response.json()})
                return response.json()
            else:
                continue

        
    def search_game(self, search_query):
        data = data = f'fields id, name, cover.url, release_dates.date, release_dates.platform, genres.name, \
                        game_modes.name, platforms.name, aggregated_rating, \
                        external_games.platform, external_games.url, external_games.category; search "{search_query}" ;\
                        where category = 0;'
        
        games = self._request_(self.games_url, data)
        names = [(game['name'], game['id']) for game in games]  # List of tuples (name, id)
        best_match = process.extractOne(search_query, names)#, scorer=process.WRatio)        
        if best_match:
            # Find the complete game data for the best match
            best_game = next(game for game in games if game['id'] == best_match[0][1])            
            best_game['cover_1080p'] = best_game['cover']['url'][2:].replace('thumb', '1080p')
            best_game['cover_720p'] = best_game['cover']['url'][2:].replace('thumb', '720p')     
            print(best_game)       
            best_game['platforms'] = [ [i['name'], datetime.utcfromtimestamp(j['date']).strftime('%Y-%m-%d')]\
                                       for i in best_game['platforms'] for j in best_game['release_dates'] if i['id']==j['platform'] and 'date' in j]

            return best_game
        else:
            print("No close matches found.")
            return None