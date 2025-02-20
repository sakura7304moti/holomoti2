from flask import Blueprint, request, jsonify
from src.route.service import twitter_service

app = Blueprint("twitter", __name__)


@app.route("/twitter/search", methods=["GET"])
def twitter_search():
    df = twitter_service.search()
    return jsonify(df.to_json(orient="records"))
