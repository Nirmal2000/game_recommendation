import markdown
from bs4 import BeautifulSoup
import re
import requests
import json
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
            break
        except:
            continue

    return api_cache[(url, params)]


def generate_answer(model, messages):
    from app import llm_cache
    messages_list = tuple([(i['role'], i['content']) for i in messages])
    if (model.model_name, messages_list) in llm_cache:
        return llm_cache[(model.model_name, messages_list)]
    result = model.invoke(messages).content
    llm_cache[(model.model_name, messages_list)] = result
    return llm_cache[(model.model_name, messages_list)]


def recommend_games(model, query, rawg):

    messages = [        
        {'role': 'system', 'content': '''You are the best Game recommendation engine in the world. \ 
Given any type of query related to recommending video games you are supposed to provide a list of games that satisfy the user's request and also explain briefly for each game why. Return the results in a numbered list.'''},
        {'role': 'user', 'content': query+' Return the results in a numbered list and explain briefly why each is a good fit in 50 words.'}
    ]
    answer = strip_markdown(generate_answer(model, messages))
    answer = re.sub(r'\[\d+\]', '', answer)
    print(answer)
    game_list = []
    for i in answer.split('\n'):
        if i:
            i = i.split(': ')
            if ': '.join(i[:-1]):
                game_list.append([': '.join(i[:-1]), i[-1]])
                
    recommended_games_info = {}
    for i,j in game_list:
        cur_game_info = rawg.search_game(i)
        cur_game_info['why'] = j
        recommended_games_info[cur_game_info['name']] = cur_game_info
        
    return recommended_games_info