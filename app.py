# install: pip install flask flask-cors
from flask import Flask
from flask_cors import CORS, cross_origin
from flask import request
from flask import jsonify
from contentBase import index
import json
import numpy
from CF import CollaborativeFiltering
from chatbot import chatbot

# Khởi tạo Flask Server Backend
app = Flask(__name__)


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        if isinstance(obj, numpy.floating):
            return float(obj)
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


# Apply Flask CORS
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/getCB', methods=['GET'])
def get_contentbase_rs():
    id = request.args.get('movieId')
    res = index.get_recommendations(int(id))
    ressult = res.to_json()
    return ressult


@app.route('/getCF', methods=['GET'])
def return_recommend():
    user_id = request.args.get('user')
    res = CollaborativeFiltering.get_recommendation_by_user(int(user_id))
    return json.dumps(res, cls=NpEncoder)


@app.route('/addDataCF', methods=['POST'])
def add_data_cf():
    user_id = int(request.args.get('user'))
    item_id = int(request.args.get('item'))
    rating = int(request.args.get('rating'))
    res = CollaborativeFiltering.update_data(user_id, item_id, rating)
    return res


@app.route('/getChatbot', methods=['GET'])
def get_res_chatbot():
    msg = request.args.get('msg')
    res = chatbot.chatbot_response(msg)
    return res


# Start Backend
if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)
