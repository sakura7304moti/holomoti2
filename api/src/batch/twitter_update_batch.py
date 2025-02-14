import os
import sys
api_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
print(api_path)
sys.path.append(api_path)

from src.route.service import twitter_service


# ----- main -----
print("twitterのDB更新バッチ処理実行中...")
twitter_service.twitter_scraping()
print("twitterのDB更新バッチ処理OK!!")