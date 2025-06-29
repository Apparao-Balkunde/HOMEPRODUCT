from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/products')
def get_products():
    return jsonify([{"name": "Homemade Pickle", "price": 150}, {"name": "Masala", "price": 80}])

if __name__ == '__main__':
    app.run(debug=True)
