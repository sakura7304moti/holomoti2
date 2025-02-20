# ----- インターフェース ----
# 検索条件クラス twitter_search_condition

# 検索結果クラス twitter_search_vo
# |_ツイートのクラス twitter_tweet_vo
# |_メディアのクラス twitter_media_vo
# |_ユーザー情報のクラス twitter_user_vo
# |_ハッシュタグのリスト twitter_hashtag_list

# メディアの種類取得結果のクラス twitter_media_type


# ----- 作成する関数 -----

# ツイートの検索(APIではページ数と結果をまとめて取得)
# ツイートの検索ページ数

# ホロライブのファンアートタグの一覧を取得

import math
from src.route.service.module.utils import const, interface

query_model = const.PsqlBase()


def _search_tweet_base(condition: interface.TwitterSearchCondition):
    query = """
        WITH T as (
        SELECT
            tw.id,
            tw.tweet_text as "tweetText",
            tw.tweet_url as "tweetUrl",
            tw.like_count as "likeCount",
            tw.user_screen_name as "userId",
            us.name as "userName",
            us.profile_image as "userImage",
            tw.created_at as "createdAt"
        FROM
            twitter.tweet AS tw
            left join twitter.user as us on tw.user_screen_name = us.screen_name
        WHERE
            1 = 1 
    """
    if condition.keyword != "":
        query += """
            AND tw.id IN (
                SELECT
                    distinct(st.id)
                FROM
                    twitter.tweet AS st
                    LEFT JOIN twitter.hashtag AS hs1 ON st.id = hs1.twitter_id
                    LEFT JOIN twitter.user AS us1 ON st.user_screen_name = us1.screen_name
                WHERE
                    st.tweet_text LIKE %(keyword)s 
                    OR hs1.hashtag LIKE %(keyword)s 
                    OR us1.screen_name LIKE %(keyword)s 
                    OR us1.name LIKE %(keyword)s 
            ) 
        """
    if condition.hashtag != "":
        query += """
            AND tw.id in (
                SELECT
                    distinct(hs.twitter_id)
                from twitter.hashtag as hs
                where 
                    hs.hashtag = %(hashtag)s
            )
        """

    if condition.like_count != 0:
        query += """
            AND tw.like_count >= %(likeCount)s 
        """

    if condition.user_id != "":
        query += """
            AND tw.user_screen_name = %(userId)s
        """
    query += " ) "  # with...)
    return query


def get_tweets(
    condition: interface.TwitterSearchCondition, page_no: int, page_size: int
):
    query = _search_tweet_base(condition)
    query += """
    SELECT
        *
    from T
    order by T."id" desc
    offset %(offset)s limit %(pageSize)s
    """
    args = condition.to_args()
    args["offset"] = max(page_no, 1) * page_size
    args["pageSize"] = page_size
    return query_model.execute_df(query, args)


def get_tweets_total_count(
    condition: interface.TwitterSearchCondition, page_size: int
) -> int:
    query = _search_tweet_base(condition)
    query += """
    SELECT
        count(*) as total
    from T
    """
    df = query_model.execute_df(query, condition.to_args())
    total = int(df["total"].iloc[0])
    return math.ceil(total / page_size)
