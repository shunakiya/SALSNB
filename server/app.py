from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

from backend import backend_blueprint
app.register_blueprint(backend_blueprint)

if __name__ == '__main__':
    app.run(host='192.168.137.221', port=5000, debug=True)