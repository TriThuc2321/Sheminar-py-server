# install: pip install flask flask-cors
from flask import Flask
from flask_cors import CORS, cross_origin
from flask import request
from flask import jsonify
import index

# Khởi tạo Flask Server Backend
app = Flask(__name__)

# Apply Flask CORS
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/getRS', methods=['POST', 'GET'])
@cross_origin(origin='*')
def multi_process():
    id = request.args.get('movieId')

    res = index.get_recommendations(int(id))
    ressult = res.to_json()
    return ressult


# Start Backend
if __name__ == '__main__':
    app.run(host='localhost', port='2321')
