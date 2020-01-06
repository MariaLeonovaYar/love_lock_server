from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app)

cluster = MongoClient('mongodb+srv://MariaLeo:provcolk13@cluster0-vfkmt.mongodb.net/test?retryWrites=true&w=majority')
db = cluster['love_lock']
values_collection = db['authorisation']
lock_collection = db['lock']

def get_data_as_response_object(username):
    response_object = {}
    results = lock_collection.find({'username': username})
    arr = []
    for el in results:
        arr.append({'_id': str(el['_id']), 'username': str(el['username']), 'size': str(el['size']), 'design': str(el['design']), 'person': str(el['person']), 'message': str(el['message'])})
    response_object['data'] = arr
    return response_object

#проверка (есть ли такой пользователь)
@app.route('/api/is_registered', methods=['GET'])
def is_registered():
    if request.method == 'GET':
        username = request.args.get('username')
        response_object = get_data_as_response_object(username)
        return jsonify(response_object)

#получение всех замков пользователя
@app.route('/api/get_user_data', methods=['GET'])
def get_user_data():
    if request.method == 'GET':
        username = request.args.get('username')
        response_object = get_data_as_response_object(username)
        return jsonify(response_object)

#регистрация пользователя
@app.route('/api/send_lock_data', methods=['POST'])
def add_input_value_into_db():
    if request.method == 'POST':
        request_data = request.get_json()
        username = request_data.get('username')
        person = request_data.get('person')
        design = request_data.get('design')
        size = request_data.get('size')
        message = request_data.get('message')
        ID = lock_collection.find().distinct('_id')
        lock_collection.insert_one({"_id": max(ID) + 1, "username": username, "person" : person, "design": design, "size": size, "message": message})
        return jsonify({})

#удаление замка по айди
@app.route('/api/delete_lock_id', methods=['POST'])
def delete_lock():
    if request.method == 'POST':
        id_lock = request.get_json().get('id_lock')
        lock_collection.delete_one({'_id': id_lock})
        return jsonify({})

#добавление нового замка
@app.route('/api/send', methods=['POST'])
def add_input_register_into_db():
    if request.method == 'POST':
        request_data = request.get_json()
        name = request_data.get('name')
        surname = request_data.get('surname')
        username = request_data.get('username')
        password = request_data.get('password')
        ID = values_collection.find().distinct('_id')
        values_collection.insert_one({"_id": max(ID)+1, "name" : name, "surname": surname, "username": username, "password": password})
        return jsonify({})

if __name__ == '__main__':
    app.run()
