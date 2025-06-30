from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient("mongodb+srv://homeadmin:<db_password>@cluster0.foywty5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["homeproductDB"]
product_collection = db["products"]

# Convert ObjectId to string
def serialize(product):
    product["_id"] = str(product["_id"])
    return product

@app.route('/')
def home():
    return "✅ HomeProduct API is running with MongoDB!"

@app.route('/api/products', methods=['GET'])
def get_products():
    products = list(product_collection.find())
    return jsonify([serialize(p) for p in products])

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.get_json()
    result = product_collection.insert_one(data)
    return jsonify({"message": "Product added", "id": str(result.inserted_id)}), 201

@app.route('/api/products/<id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    product_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    return jsonify({"message": "Product updated"})

@app.route('/api/products/<id>', methods=['DELETE'])
def delete_product(id):
    product_collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Product deleted"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
