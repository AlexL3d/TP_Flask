from flask import Flask, request, jsonify
from pymongo import MongoClient

# # Connexion à la base de données MongoDB
client = MongoClient('mongodb://localhost:27017/',username='root',password='root',authSource='admin')
db = client[Bdd_user]
collection = db[users]

app = Flask(__name__)

@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.get_json()
    user = {
        'name': user_data['name'],
        'id': user_data['id'],
        'email': user_data['email']
    }
    result = collection.insert_one(user)
    return jsonify({'message': 'User created successfully', 'user_id': str(result.inserted_id)})

@app.route('/', methods=['GET'])
@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = collection.find_one({'_id': ObjectId(user_id)})
    if user:
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.get_json()
    updated_user = {
        'name': user_data['name'],
        'id': user_data['id'],
        'email': user_data['email']
    }
    result = collection.update_one(
        {'_id': ObjectId(user_id)}, {'$set': updated_user})
    if result.modified_count > 0:
        return jsonify({'message': 'User updated successfully'})
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = collection.delete_one({'_id': ObjectId(user_id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'message': 'User not found'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
