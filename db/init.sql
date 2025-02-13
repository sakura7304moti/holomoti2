-- スキーマ作成
CREATE SCHEMA IF NOT EXISTS twitter;

-- テーブル作成
CREATE TABLE IF NOT EXISTS twitter.tweet (
	id int8 NOT NULL,
	tweet_text text,
	tweet_url text,
	like_count int4,
	user_screen_name text,
	created_at timestamptz,
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS twitter.hashtag (
	twitter_id int8 NOT NULL,
	hashtag text,
	CONSTRAINT twitter_hashtag_twitter_id_fkey 
	FOREIGN KEY (twitter_id) REFERENCES twitter.tweet(id)
);

CREATE TABLE IF NOT EXISTS twitter.media (
	twitter_id int8 NOT NULL,
	media_type text,
	media_url text,
	thumbnail_url text,
    CONSTRAINT twitter_media_twitter_id_fkey 
    FOREIGN KEY (twitter_id) 
    REFERENCES twitter.tweet(id)
);

CREATE TABLE IF NOT EXISTS twitter.user (
	screen_name text,
	name text,
	profile_image text,
	updated_at timestamptz
);