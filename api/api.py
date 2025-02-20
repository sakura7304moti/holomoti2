"""
Flask Server
"""

from flask import Flask
from flask_cors import CORS

"""
services
"""
from src.route import twitter_route

"""
Flask run
"""
app = Flask(__name__)
CORS(app)

"""
import apps
"""
app.register_blueprint(twitter_route.app)

"""
api run
"""
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
