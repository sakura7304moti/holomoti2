import psycopg2
import pandas as pd
import os


from sqlalchemy import create_engine
from urllib.parse import urlparse


class Option:
    def _root_path(self):
        path = os.path.abspath(__file__)
        for _ in range(6):
            path = os.path.dirname(path)
        return path

    def _option_path(self):
        return os.path.join(self._root_path(), "option")

    def holo_names(self):
        """
        ホロライブのファンアート一覧
        """
        return os.path.join(self._option_path(), "holo_names.csv")

class PsqlBase:
    def db_url(self):
        """
        接続URL
        """
        return 'postgresql+psycopg2://sakura0moti:music0@postgres_db/holomoti'

    def db_pd_connection(self):
        """
        read_sql用の接続情報
        """
        return create_engine(self.db_url())

    def db_psql_connection(self):
        """
        コミット用の接続情報
        """
        url = self.db_url()
        # URLを解析
        parsed_url = urlparse(url)

        # 必要な情報を取得
        username = parsed_url.username
        password = parsed_url.password
        hostname = parsed_url.hostname
        db_name = parsed_url.path[1:]
        return psycopg2.connect(
            host=hostname, dbname=db_name, user=username, password=password
        )

    def execute_commit(self, query: str, param: dict | None = None):
        """
        クエリを実行するだけ。commitが必要な場合はこっち。
        """
        with self.db_psql_connection() as con:
            cur = con.cursor()
            if param is None:
                cur.execute(query)
            else:
                cur.execute(query, param)

            con.commit()

    def execute_df(self, query: str, param: dict | None = None):
        """
        クエリを実行してデータフレームを取得
        """
        if param is None:
            return pd.read_sql(sql=query, con=self.db_pd_connection())
        else:
            return pd.read_sql(sql=query, con=self.db_pd_connection(), params=param)

    def current_time(self):
        """
        現在の日時を取得。
        create_atやupdate_atの日時セットに。
        """
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")