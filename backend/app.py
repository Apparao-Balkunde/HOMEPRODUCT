from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory product list
products = [
    {"id": 1, "name": "Pickle", "price": 150},
    {"id": 2, "name": "Masala", "price": 80}
]

# Root route for testing on browser
@app.route('/')
def home():
    return "✅ HomeProduct API is running!"

# Get all products
@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify(products)

# Add new product
@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.get_json()
    new_id = max([p["id"] for p in products]) + 1 if products else 1
    data["id"] = new_id
    products.append(data)
    return jsonify({"message": "Product added", "product": data}), 201

# Update existing product
@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    for p in products:
        if p["id"] == product_id:
            p.update(data)
            return jsonify({"message": "Product updated", "product": p})
    return jsonify({"error": "Product not found"}), 404

# Delete a product
@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    global products
    products = [p for p in products if p["id"] != product_id]
    return jsonify({"message": "Product deleted"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
