from flask import Flask, jsonify, request
import os
from langchain_openai import ChatOpenAI
from utils import recommend_games
from flask_cors import CORS
import pickle
from rawg import RAWG

llm_cache = pickle.load(open('./files/llm_cache.pkl', 'rb'))
api_cache = pickle.load(open('./files/api_cache.pkl', 'rb'))
pp_model = ChatOpenAI(temperature=0, 
                   base_url='https://api.perplexity.ai', 
                   api_key=os.environ['PERPLEXITY_API_KEY'],
                  model='llama-3-sonar-large-32k-online')
rawg = RAWG(os.environ['RAWG_API_KEY'])

app = Flask(__name__)
CORS(app)

@app.route('/recommend', methods=['GET'])
def recommend():
    user_query = request.args.get('query', default='', type=str)
    return jsonify(recommend_games(pp_model, user_query, rawg))

if __name__ == '__main__':
    app.run(debug=True)
