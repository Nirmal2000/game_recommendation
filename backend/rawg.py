from utils import handle_get_requests
import json

class RAWG:
    def __init__(self, api_key):
        self.ak = api_key
        self.games_url = 'https://api.rawg.io/api/games'
    def search_game(self, query):
        params = {
            'key': self.ak,
            'page': 1,           # Specify which page of results to return
            'page_size': 10,     # Specify the number of results per page
            'search': query,
            
        }
        response = handle_get_requests(self.games_url, params).content
        response = json.loads(response)['results'][0]
        stores = self.get_stores(response['id'])
        new_stores = {}
        for i in stores:
            if 'steampowered' in i['url']:
                new_stores['PC'] = i['url']
            elif 'microsoft.' in i['url']:
                new_stores['Xbox'] = i['url']
            elif 'playstation.' in i['url']:
                new_stores['PlayStation'] = i['url']
            elif 'nintendo'  in i['url']:
                new_stores['Switch'] = i['url']
        

        for idx, i in enumerate(response['parent_platforms']):
            if i['platform']['name'] in new_stores:
                response['parent_platforms'][idx]['platform']['url'] = new_stores[i['platform']['name']]
        return response
    
    def get_stores(self, gameId):
        params = {
            'key': self.ak,            
        }
        response = handle_get_requests(self.games_url+f"/{gameId}/stores", params).content        
        return json.loads(response)['results']