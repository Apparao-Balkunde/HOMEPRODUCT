# ✅ app.py (Flask Backend with MongoDB & JWT Auth)

from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import bcrypt
import jwt
import datetime
import os

app = Flask(__name__)
Cors = CORS(app)

SECRET_KEY = "secret123"

client = MongoClient("mongodb+srv://homeadmin:<db_password>@cluster0.foywty5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["homeproductDB"]
product_collection = db["products"]
user_collection = db["users"]

def serialize(product):
    product["_id"] = str(product["_id"])
    return product

def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token missing"}), 401
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except:
            return jsonify({"error": "Invalid token"}), 403
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/')
def home():
    return "✅ HomeProduct API is running with MongoDB!"

@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    password = data['password']
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    user_collection.insert_one({"email": email, "password": hashed})
    return jsonify({"message": "User registered"})

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = user_collection.find_one({"email": data['email']})
    if user and bcrypt.checkpw(data['password'].encode(), user['password']):
        token = jwt.encode({"email": user['email'], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)}, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/products', methods=['GET'])
def get_products():
    products = list(product_collection.find())
    return jsonify([serialize(p) for p in products])

@app.route('/api/products', methods=['POST'])
@token_required
def add_product():
    data = request.get_json()
    result = product_collection.insert_one(data)
    return jsonify({"message": "Product added", "id": str(result.inserted_id)}), 201

@app.route('/api/products/<id>', methods=['PUT'])
@token_required
def update_product(id):
    data = request.get_json()
    product_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    return jsonify({"message": "Product updated"})

@app.route('/api/products/<id>', methods=['DELETE'])
@token_required
def delete_product(id):
    product_collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Product deleted"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
