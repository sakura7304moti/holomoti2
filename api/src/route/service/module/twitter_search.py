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
import pandas as pd
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
            TO_CHAR(tw.created_at, 'YYYY-MM-DD') as "createdAt"
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


def _get_tweets(
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
    args["offset"] = (max(page_no, 1) - 1) * page_size
    args["pageSize"] = page_size
    return query_model.execute_df(query, args)


def _get_tweets_total_count(
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


def _get_media_base(ids: list[int]):
    """
    ツイートのIDのリスト -> メディアのリスト
    """
    if len(ids) == 0:
        return pd.DataFrame(
            columns=["twitterId", "mediaType", "mediaUrl", "thumbnailUrl"]
        )

    where = f"({', '.join(map(str, ids))}) "
    query = """
        SELECT
            twitter_id as "twitterId",
            media_type as "mediaType",
            media_url as "mediaUrl",
            thumbnail_url as "thumbnailUrl"
        from twitter.media
        where twitter_id in 
    """
    query += where
    query += "order by twitter_id, media_url"
    return query_model.execute_df(query)


def _get_user_base(ids: list[str]):
    """
    ユーザーのIDのリスト -> ユーザー情報
    """
    if len(ids) == 0:
        return pd.DataFrame(columns=["userId", "userName", "userImage"])
    where = " ({}) ".format(", ".join(f"'{item}'" for item in ids))
    query = """
        SELECT
            screen_name as "userId",
            name as "userName",
            profile_image as "userImage"
        from twitter.user
        where screen_name in 
    """
    query += where
    query += "order by screen_name"
    return query_model.execute_df(query)


def _get_hashtag_base(ids: list[int]):
    """
    ツイートのIDのリスト -> ハッシュタグのリスト
    """
    if len(ids) == 0:
        return pd.DataFrame(columns=["twitterId", "hashtag"])

    where = f"({', '.join(map(str, ids))}) "
    query = """
    SELECT
        twitter_id as "twitterId",
        hashtag
    from twitter.hashtag
    where twitter_id in 
    """
    query += where
    query += "order by twitter_id, hashtag"
    return query_model.execute_df(query)


def search(condition: interface.TwitterSearchCondition, page_no: int, page_size: int):

    df = _get_tweets(condition, page_no, page_size)
    total_count = _get_tweets_total_count(condition, page_size)

    ids = df["id"].to_list()
    media_df = _get_media_base(ids)

    user_ids = df["userId"].to_list()
    user_df = _get_user_base(user_ids)

    hashtag_df = _get_hashtag_base(ids)

    # 検索結果でまとめる
    records = []
    for _, row in df.iterrows():
        row_dict = {}

        # tweet
        tweet_dict = row.to_dict()
        row_dict["tweet"] = tweet_dict

        # media
        media_dict = media_df[media_df["twitterId"] == int(row["id"])].to_dict(
            orient="records"
        )
        for m in media_dict:
            m.pop("twitterId")
        row_dict["media"] = media_dict

        # user
        user_dict = user_df[user_df["userId"] == str(row["userId"])].iloc[0].to_dict()
        row_dict["user"] = user_dict

        # hashtag
        hashtag_dict = hashtag_df[hashtag_df["twitterId"] == int(row["id"])][
            "hashtag"
        ].to_list()
        row_dict["hashtags"] = hashtag_dict

        # tweet key remove
        row_dict["tweet"].pop("userId")

        # save
        records.append(row_dict)
    return {"records": records, "totalCount": total_count}
