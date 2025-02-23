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


def _to_search_df(df: pd.DataFrame, total_count: int):
    """
    tweet df -> search result
    """
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


def search(condition: interface.TwitterSearchCondition, page_no: int, page_size: int):
    df = _get_tweets(condition, page_no, page_size)
    total_count = _get_tweets_total_count(condition, page_size)
    return _to_search_df(df, total_count)


def top_medias():
    query = """
    SELECT
        t.id,
        t.tweet_text AS "tweetText",
        t.tweet_url AS "tweetUrl",
        t.like_count AS "likeCount",
        t.user_screen_name AS "userId",
        TO_CHAR(t.created_at, 'YYYY-MM-DD') AS "createdAt"
    FROM
        twitter.tweet AS t
    WHERE
        t.id IN (
            SELECT
                id
            FROM
                twitter.tweet AS tw
            WHERE
                tw.created_at > CURRENT_TIMESTAMP - cast('2 weeks' AS INTERVAL)
                and tw.like_count > 1000
            ORDER BY
                random()
            LIMIT
                12
        )
    """
    df = query_model.execute_df(query)
    total_count = 1
    return _to_search_df(df, total_count)


def hot_users():
    query = """
    with before_user as (
        SELECT
        *
    FROM
        (
            SELECT
                user_screen_name AS "userId",
                avg(like_count) AS "likeCount"
            FROM
                twitter.tweet
            WHERE
                created_at < CURRENT_TIMESTAMP - cast('2 weeks' AS INTERVAL)
                AND CURRENT_TIMESTAMP - cast('1 months' AS INTERVAL) < created_at
            GROUP BY
                user_screen_name
        )
    ),
    after_user as (
        SELECT
        *
    FROM
        (
            SELECT
                user_screen_name AS "userId",
                avg(like_count) AS "likeCount"
            FROM
                twitter.tweet
            WHERE
                created_at > CURRENT_TIMESTAMP - cast('2 weeks' AS INTERVAL)
            GROUP BY
                user_screen_name
        )
    ),
    hot_user as (
        SELECT
        *
    from after_user
    WHERE
        EXISTS
            (
                SELECT
                    1
                from before_user
                WHERE
                    before_user."userId" = after_user."userId"
                    AND (after_user."likeCount" - before_user."likeCount") > 5000
            )
        order by random()
        limit 5
    ),
    A as (
        SELECT
            t.id,
            t.tweet_text AS "tweetText",
            t.tweet_url AS "tweetUrl",
            t.like_count AS "likeCount",
            t.user_screen_name AS "userId",
            TO_CHAR(t.created_at, 'YYYY-MM-DD') AS "createdAt",
            row_number() over (partition by t.user_screen_name order by t.created_at desc) as "rank"
        FROM
            twitter.tweet AS t
        WHERE
            EXISTS
                (
                    SELECT
                        1
                    from hot_user
                    where 
                        t.user_screen_name = hot_user."userId"
                )
            and t.like_count > 5000
        order by t.user_screen_name, t.created_at desc
    )
    SELECT
        *
    from A
    where A."rank" < 3
    """
    df = query_model.execute_df(query)
    total_count = 1
    return _to_search_df(df, total_count)
