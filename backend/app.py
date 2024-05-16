from flask import Flask, jsonify, request, redirect, url_for, session, render_template, abort
from authlib.integrations.flask_client import OAuth
import json
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from utils import recommend_games
from flask_cors import CORS
import pickle
from rawg import RAWG
from datetime import datetime
from flask_pymongo import PyMongo
from functools import wraps
from igdb import IGDB

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGGSMITH_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = "GameReco"

pp_model = ChatOpenAI(temperature=0, 
                   base_url=os.environ['OPENAI_BASE_URL'],
                   api_key=os.environ['PERPLEXITY_API_KEY'],
                  model='llama-3-sonar-large-32k-online')
rawg = RAWG(os.environ['RAWG_API_KEY'])
igdb = IGDB(os.environ['IGDB_CID'], os.environ['IGDB_BEARER'])


appConf = {
    "OAUTH2_CLIENT_ID": os.environ['GGL_CLIENT_ID'],
    "OAUTH2_CLIENT_SECRET": os.environ['GGL_CLIENT_SECRET'],
    "OAUTH2_META_URL": "https://accounts.google.com/.well-known/openid-configuration",
    "FLASK_SECRET": os.environ['GUID'],
    "FLASK_PORT": 5001,
}

app = Flask(__name__)
app.config["MONGO_URI"] = os.environ['MONGO_URI']
app.secret_key = appConf.get("FLASK_SECRET")

CORS(app)
mongo = PyMongo(app)
oauth = OAuth(app)

oauth.register(
    "GameReco",
    client_id=appConf.get("OAUTH2_CLIENT_ID"),
    client_secret=appConf.get("OAUTH2_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'{appConf.get("OAUTH2_META_URL")}',
)

## AUTH SECTION
@app.route("/google-login")
def googleLogin():    
    if 'user' in session:
        print("LOGGED IN ")
    return oauth.GameReco.authorize_redirect(redirect_uri=url_for("googleCallback", _external=True))

@app.route("/signin-google")
def googleCallback():
    print("SIGNING")
    token = oauth.GameReco.authorize_access_token()

    user_info = token.get('userinfo')
    print('->',user_info)
    # user_info = resp.json()

    user = mongo.db.users.find_one({"email": user_info['email']})
    if not user:
        user = {
            "name": user_info['name'],
            "email": user_info['email'],
            "createdDate": datetime.now(),
            "dp": user_info['picture']
        }
        mongo.db.users.insert_one(user)    

    session['user'] = token
    print(session['user'])
    return redirect(f'http://localhost:3000')


@app.route("/logout")
def logout():
    print("LOGOUT")
    session.pop("user", None)
    return redirect("http://localhost:3000")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'error': 'Authentication required'}), 401  # Unauthorized
        return f(*args, **kwargs)
    return decorated_function

## AUTH SECTION ENDS

@app.route('/')
def index():
    return render_template('home.html', session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))


@app.route('/recommend', methods=['GET', 'POST'])
# @login_required
def recommend():
    # user_query = request.args.get('query', default='', type=str)
    data = request.json
    user_query = data.get('query')
    user_email = data.get('email')
    mongo.db.queries.insert_one({'email':user_email, 'query': user_query})
    return jsonify(recommend_games(pp_model, user_email, user_query, igdb, mongo))

@app.route('/history', methods=['POST'])
def history():
    data = request.json
    mongo_response = mongo.db.queries.find({'email': data.get('email')})
    return mongo_response


@app.route('/submit_feedback', methods=['POST'])
# @login_required
def submit_feedback():
    # Retrieve data from POST request
    data = request.json
    query = data.get('query')
    feedback_text = data.get('feedback')
    email =  data.get('email')
    
    if not query or not feedback_text:
        return jsonify({'error': 'Missing required fields'}), 400
    
    feedback_entry = {
        'query': query,
        'feedback': feedback_text,
        'createdDate': datetime.now(),
        'email': email
    }
    mongo.db.feedback.insert_one(feedback_entry)

    return jsonify({'message': 'Feedback submitted successfully'}), 201


@app.route('/like_dislike', methods=['POST'])
def like_dislike():
    # Retrieve data from POST request
    data = request.json
    key = data.get('key', None)
    value = data.get('value', None)
    email = data.get('email')
    game_name = data.get('game_name')    

    filter = {'email': email, 'gameName': game_name}

    update = {
        '$set': {
            key: value,
            'updatedDate': datetime.utcnow()  # Adds or updates the updatedDate field
        },
        '$setOnInsert': {
            'createdDate': datetime.utcnow()  # Sets createdDate only if it's a new document
        }
    }
    result = mongo.db.likes.update_one(filter, update, upsert=True)

    # Insert like or dislike into the MongoDB
    if result.matched_count > 0 or result.upserted_id is not None:
        return jsonify({'message': 'Action recorded successfully'}), 201
    else:
        return jsonify({'message': 'Failed to record action'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=appConf.get('FLASK_PORT'), host='0.0.0.0')
