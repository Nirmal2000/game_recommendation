import markdown
from bs4 import BeautifulSoup
import re
import requests
import json
import re
import pickle
import time

def strip_markdown(md):
    html = markdown.markdown(md)
    soup = BeautifulSoup(html, features='html.parser')
    return soup.get_text()

def handle_get_requests(url, params):
    from app import api_cache
    params = tuple([(i,j) for i,j in params.items()])
    if (url, params) in api_cache:
        return api_cache[(url, params)]
    while 1:
        try:
            api_cache[(url, params)] = requests.get(url, params)
            json.loads(api_cache[(url, params)].content)
            # time.sleep(0.5)
            pickle.dump(api_cache, open('./files/api_cache.pkl', 'wb'))
            break
        except:
            continue

    return api_cache[(url, params)]


def generate_answer(model, messages):
    from app import mongo
    # messages_list = tuple([(i['role'], i['content']) for i in messages])
    mongo_response = mongo.db.llm_cache.find_one({'model_name': model.model_name, 'messages': messages})
    if mongo_response:
        return mongo_response['response']
    result = model.invoke(messages).content
    mongo.db.llm_cache.insert_one({'model_name': model.model_name, 'messages': messages, 'response': result})
    return result

def parse_answer(answer):
    pattern = r"{(.*?)}"
    
    # Using re.findall to find all occurrences
    matches = re.findall(pattern, answer, re.DOTALL)
    return json.loads('{'+matches[0]+'}')

def recommend_games(model, email, query, igdb, mongo):

    messages = [        
        {'role': 'user', 'content': "Query: " + query+'''\n\nRecommend at least 7 games. DO NOT recommend games already mentioned in the query. Explain briefly why each game is a good fit in at least 100 words and also assign a score on a scale of 1-100 that indicates how much of a good fit they are to my query. Return the results in the following JSON format
```json
{"game_1": [score, reason], "game_2": [score, reason]}
```'''}
    ]
    answer = strip_markdown(generate_answer(model, messages))
    answer = re.sub(r'\[\d+\]', '', answer)
    print(answer)
    game_list = parse_answer(answer)    
    recommended_games_info = {}
    for i,[j,k] in game_list.items():
        cur_game_info = igdb.search_game(i)
        cur_game_info['reco_score'] = j
        cur_game_info['reco_reason'] = k        
        existing_info = mongo.db.likes.find_one({'email': email, 'gameName': cur_game_info['name']})
        
        if existing_info:
        # Dictionary comprehension to exclude specific keys
            filtered_info = {key: value for key, value in existing_info.items() if key not in ['email', 'createdDate', 'updatedDate', '_id']}
            cur_game_info.update(filtered_info)
        recommended_games_info[cur_game_info['name']] = cur_game_info

    recommended_games_info = sorted(recommended_games_info.items(), reverse=True, key=lambda x:x[1]['reco_score'])    
    print(recommended_games_info)
    return recommended_games_info