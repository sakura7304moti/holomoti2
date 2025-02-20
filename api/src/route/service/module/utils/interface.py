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


class TwitterTweetVo:
    """
    ツイート
    """

    def __init__(self, id: int, tweet_text: str, tweet_url: str, like_count: int):
        self.id = id
        self.tweet_text = tweet_text
        self.tweet_url = tweet_url
        self.like_count = like_count


class TwitterMediaVo:
    """
    メディア
    """

    def __init__(
        self, tweet_id: int, media_type: str, media_url: str, thumbnail_url: str
    ):
        self.tweet_id = tweet_id
        self.media_type = media_type
        self.media_url = media_url
        self.thumbnail_url = thumbnail_url


class TwitterUserVo:
    """
    ユーザー
    """

    def __init__(self, user_id: str, user_name: str, user_image: str):
        self.user_id = user_id
        self.user_name = user_name
        self.user_image = user_image


class TwitterSearchVo:
    """
    ツイートの検索結果
    """

    def __init__(self, tweet, medias: list[TwitterMediaVo], user: TwitterUserVo):
        self.tweet = tweet
        self.medias = medias
        self.user = user
