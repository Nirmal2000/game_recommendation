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
        return json.loads(response)['results'][0]