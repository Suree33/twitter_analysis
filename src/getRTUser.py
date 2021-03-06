from time import sleep
import pandas as pd
from requests_oauthlib import OAuth1Session
import json
import csv

CK = "TXNqxXBPleGVaiaADTFtExEjP"  # Consumer key
CS = "SeiperIaqwssdInX9LClBPfpKeeqi3nY32ur0p7EFbMZRgP0J9"  # Consumer secret
AT = "972830233253445633-4ZMbbSNGurouSa7FOb1NR1i972hgbv7"  # Access token
ATS = "lms33b0Z4Nv6sIKByEf96FYsq3hLDSq1zDsKNSEmb6dCz"  # Access token secret


max_id = -1
url = 'https://api.twitter.com/1.1/search/tweets.json'

'''
keyword = '' #検索キーワード設定
'''
# 検索ツイート
original_tweet = '来週、日本時間1月13日（水）3:00AMにRazerStore LIVE CES Editionが開催されます。'
# 元ユーザー表示名
original_tweet_screen_name = '@RazerJP'

'''
CSVファイル準備
'''
# 取得した値を格納ファイル名
output_csv_file_name = 'RT/' + original_tweet_screen_name.lstrip('@') + \
    '/retweet_info' + original_tweet_screen_name + '.csv'

with open(output_csv_file_name, 'a') as f:
    writer = csv.writer(f, lineterminator='\n')
    header = ['ユーザー名', 'ユーザー表示名', 'ユーザーID', 'リツイートID', '時間', 'ツイート']
    writer.writerow(header)

# リツイート検索限定
keyword = original_tweet + ' filter:retweets ' + original_tweet_screen_name

count = 100
params = {'q': keyword, 'count': count, 'max_id': max_id}

url = "https://api.twitter.com/1.1/search/tweets.json"
twitter = OAuth1Session(CK, CS, AT, ATS)
req = twitter.get(url, params=params)


columns = ['ユーザー名', 'ユーザー表示名', 'ユーザーID', 'リツイートID', '時間', 'ツイート']
df = pd.DataFrame(columns=columns)

i = 0  # JSON位置
while(True):
    if max_id != -1:
        params['max_id'] = max_id - 1
    req = twitter.get(url, params=params)

    if req.status_code == 200:
        search_timeline = json.loads(req.text)
        i += 1

        if search_timeline['statuses'] == []:
            break

        for tweet in search_timeline['statuses']:
            user_name = tweet['user']['name']
            user_screen_name = tweet['user']['screen_name']
            user_id = tweet['user']['id']
            retweet_id = tweet['id']
            created_at = tweet['created_at']
            text = tweet['text']

            append_list = [user_name, user_screen_name,
                           user_id, retweet_id, created_at, text]

            df_next = pd.DataFrame(
                [append_list],
                columns=columns
            )

            df = df.append(df_next)
            max_id = search_timeline['statuses'][-1]['id']

            with open(output_csv_file_name, 'a') as f:
                writer = csv.writer(f, lineterminator='\n')
                writer.writerow(append_list)

    else:
        print('1５分待ちます')
        sleep(15 * 60)

'''
データフレームの確認用
'''
print('dataframeの行数・列数の確認==>\n', df.shape)
print('indexの確認==>\n', df.index)
print('columnの確認==>\n', df.columns)
print('dataframeの各列のデータ型を確認==>\n', df.dtypes)

df.head()
