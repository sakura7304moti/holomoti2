from src.route.service.module import twitter_update

# ツイッターのdbの更新
def twitter_scraping():
    twitter_update.update()

# ツイッターのdbの更新テスト
def twitter_scraping_test():
    twitter_update.test()