from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/api/books')
def get_books():
    return jsonify({
        "books": [
            "Book 1",
            "Book 2",
            "Book 3"
        ]
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
