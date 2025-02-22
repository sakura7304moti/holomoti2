import pandas as pd


from flask import Blueprint, request, jsonify
from src.route.service import twitter_service
from src.route.service.module.utils import interface, const

app = Blueprint("twitter", __name__)

PAGE_SIZE = 20


def to_search_condition():
    """
    検索条件を取得
    """
    json_data = request.json
    keyword = json_data.get("keyword", "")
    hashtag = json_data.get("hashtag", "")
    like_count_text = str(json_data.get("likeCount", "0"))
    like_count = int(like_count_text) if like_count_text.isdecimal() else 0
    user_id = json_data.get("userId", "")
    return interface.TwitterSearchCondition(keyword, hashtag, like_count, user_id)


def get_page_no():
    """
    クエリパラメータのページ番号を取得
    """
    page_no = 1
    if request.args.get("page") is not None:
        if str(request.args.get("page")).isdecimal():
            page_no = int(request.args.get("page"))

    if page_no < 1:
        page_no = 1
    return page_no


@app.route("/twitter/search", methods=["POST"])
def twitter_search():
    page_no = get_page_no()
    condition = to_search_condition()
    result = twitter_service.search(condition, page_no, PAGE_SIZE)
    return jsonify(result)


@app.route("/twitter/tags", methods=["GET"])
def twitter_tags():
    opt = const.Option()
    df = pd.read_csv(opt.holo_names())
    records = df.to_dict(orient="records")
    return jsonify(records)
