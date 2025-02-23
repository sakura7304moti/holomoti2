"""
twitter
"""


class TwitterSearchCondition:
    """
    検索条件
    """

    def __init__(self, keyword: str, hashtag: str, like_count: int, user_id: int):
        self.keyword = keyword
        self.hashtag = hashtag
        self.like_count = like_count
        self.user_id = user_id

    def to_args(self):
        return {
            "keyword": f"%{self.keyword}%",
            "hashtag": self.hashtag,
            "likeCount": self.like_count,
            "userId": self.user_id,
        }
