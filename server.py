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

# http://127.0.0.1/add
# http://127.0.0.1/minus
# http://127.0.0.1/multi
# http://127.0.0.1/div


@app.route('/add', methods=['POST', 'GET'])
@cross_origin(origin='*')
def add_process():
    a = int(request.args.get('sothunhat'))
    b = int(request.args.get('sothuhai'))
    kq = a + b
    return 'Kết quả là: ' + str(kq)


@app.route('/minus', methods=['POST', 'GET'])
@cross_origin(origin='*')
def minus_process():
    a = int(request.args.get('sothunhat'))
    b = int(request.args.get('sothuhai'))
    kq = a - b
    return 'Kết quả là: ' + str(kq)


@app.route('/div', methods=['POST', 'GET'])
@cross_origin(origin='*')
def div_process():
    return "Hàm chia"


@app.route('/viethoa', methods=['POST'])
@cross_origin(origin='*')
def viethoa_process():
    s = request.form.get("chuoiinput")
    #s = request.args.get("chuoiinput")
    return s.upper()


@app.route('/getRS', methods=['POST', 'GET'])
@cross_origin(origin='*')
def multi_process():
    name = request.args.get('movie')
    res = index.get_recommendations(name)
    ressult = res.to_json()
    return ressult


# Start Backend
if __name__ == '__main__':
    app.run(host='localhost', port='2321')
