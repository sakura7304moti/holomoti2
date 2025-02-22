from src.route.service.module.utils import interface
from src.route.service.module import twitter_update, twitter_search


# ツイッターのdbの更新
def twitter_scraping():
    twitter_update.update()


# ツイッターのdbの更新テスト
def twitter_scraping_test():
    twitter_update.test()


def search(condition: interface.TwitterSearchCondition, page_no: int, page_size: int):
    return twitter_search.search(condition, page_no, page_size)
