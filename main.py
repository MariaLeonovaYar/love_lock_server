from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from gunicorn import app

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)


CORS(app)

cluster = MongoClient('mongodb+srv://MariaLeo:provcolk13@cluster0-vfkmt.mongodb.net/test?retryWrites=true&w=majority')
db = cluster['love_lock']
values_collection = db['authorisation']
lock_collection = db['lock']

def get_lock_data_as_response_object(username):
    response_object = {}
    results = lock_collection.find({'username': username})
    arr = []
    for el in results:
        arr.append({'_id': str(el['_id']),'username': str(el['username']), 'person': str(el['person']), 'design': str(el['design']), 'message': str(el['message']), 'size': str(el['size'])})
    response_object['data'] = arr
    return response_object

@app.route('/api/get_lock_data', methods=['GET'])
def get_lock_data():
    if request.method == 'GET':
        username = request.args.get('username')
        response_object = get_lock_data_as_response_object(username)
        return jsonify(response_object)

@app.route('/api/send_lock_data', methods=['POST'])
def send_lock_data():
    if request.method == 'POST':
        request_data = request.get_json()
        username = request_data.get('username')
        person = request_data.get('person')
        design = request_data.get('design')
        size = request_data.get('size')
        message = request_data.get('message')
        ID = lock_collection.find().distinct('_id')
        if (lock_collection.find().distinct('_id')):
            ID = 30
#              ID = (max(lock_collection.find().distinct('_id')), 10)+1
#         else:
#             ID = 0
        lock_collection.insert_one({"username": username, "person" : person, "design": design, "size": size, "message": message})
        return jsonify({})

@app.route('/login', methods=['POST'])
def login():
    users = db['authorisation']
    response_object = {}
    request_data = request.get_json()
    username = request_data.get('username')
    password = request_data.get('password')
    login_user = users.find_one({'username' : str(username)})
    if login_user:
        if str(password) == login_user['password']:
            response_object['message'] = str('true')
            return jsonify(response_object)
    response_object['message'] = str('false')
    return jsonify(response_object)

@app.route('/register', methods=['POST'])
def register():
    users = db['authorisation']
    
    request_data = request.get_json()
    name = request_data.get('name')
    surname = request_data.get('surname')
    username = request_data.get('username')
    password = request_data.get('password')
    response_object = {}
    existing_user = users.find_one({'username' : str(username)})
    #if (users.find().distinct('_id')):
     #   ID = int(str(max(users.find().distinct('_id'))), 10)+1
   # else:
    #    ID = 0

    if existing_user:
         response_object['message'] = str('false')
         return jsonify(response_object)
    users.insert_one({'name' : name,'surname' : surname,'username' : username, 'password' : password})
    response_object['message'] = str('true')
    return jsonify(response_object)

@app.route('/api/delete_lock_id', methods=['POST'])
def delete_lock():
    if request.method == 'POST':
        id_lock = request.get_json().get('id_lock')
        lock_collection.delete_one({'_id': id_lock})
        return jsonify({})

if __name__ == '__main__':
    app.run()
