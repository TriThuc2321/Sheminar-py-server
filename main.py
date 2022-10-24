# install: pip install flask flask-cors
from asyncio.windows_events import NULL
from flask import Flask
from flask_cors import CORS, cross_origin
from flask import request
from flask import jsonify
from contentBase import index
import json
import numpy
from CF import CollaborativeFiltering

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


@app.route('/', methods=['GET'])
@cross_origin(origin='*')
def get_contentbase_rs():
    id = request.args.get('movieId')
    if (id == NULL):
        id = 19995
    res = index.get_recommendations(int(id))
    ressult = res.to_json()
    return ressult


@app.route('/getCF', methods=['GET'])
@cross_origin(origins='*')
def return_recommend():
    user_id = request.args.get('user')
    res = CollaborativeFiltering.get_recommendation_by_user(int(user_id))
    return json.dumps(res, cls=NpEncoder)


@app.route('/addDataCF', methods=['POST'])
@cross_origin(origins='*')
def add_data_cf():
    user_id = int(request.args.get('user'))
    item_id = int(request.args.get('item'))
    rating = int(request.args.get('rating'))
    res = CollaborativeFiltering.update_data(user_id, item_id, rating)
    return res


# Start Backend
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
