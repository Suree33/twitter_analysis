from time import sleep
import pandas as pd
import json
import csv
from requests_oauthlib import OAuth1Session
import tweepy


def get_rt(tweet: str, tweet_user_id: str, filename: str):
    """"tweet"をリツイートした人のリストを取得して、filenameに保存する。

    Args:
        tweet (str): 検索に使われる、ツイート本文。改行は含められない
        tweet_user_id (str): ユーザーID
        filename (str): 保存先ファイル名
    """

    if not tweet_user_id.startswith('@'):
        tweet_user_id = '@' + tweet_user_id

    # Consumer key
    CK = "TXNqxXBPleGVaiaADTFtExEjP"
    # Consumer secret
    CS = "SeiperIaqwssdInX9LClBPfpKeeqi3nY32ur0p7EFbMZRgP0J9"
    # Access token
    AT = "972830233253445633-4ZMbbSNGurouSa7FOb1NR1i972hgbv7"
    # Access token secret
    ATS = "lms33b0Z4Nv6sIKByEf96FYsq3hLDSq1zDsKNSEmb6dCz"

    max_id = -1
    url = 'https://api.twitter.com/1.1/search/tweets.json'

    '''
    CSVファイル準備
    '''
    # 取得した値を格納するファイル名
    output_csv_file_name = filename

    with open(output_csv_file_name, 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        header = ['ユーザー名', 'ユーザー表示名', 'ユーザーID', 'リツイートID', '時間', 'ツイート']
        writer.writerow(header)

    # リツイート検索限定
    keyword = tweet + ' filter:retweets ' + tweet_user_id

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


def get_follower(user_id: str, filename: str):
    """user_idのフォロワーを取得し、filenameに保存する。

    Args:
        user_id (str): TwitterのユーザーID
        filename (str): 保存先ファイル名
    """
    # Consumer key
    consumer_key = 'TXNqxXBPleGVaiaADTFtExEjP'
    # Consumer secret
    consumer_secret = 'SeiperIaqwssdInX9LClBPfpKeeqi3nY32ur0p7EFbMZRgP0J9'
    # Access token
    access_token = '972830233253445633-4ZMbbSNGurouSa7FOb1NR1i972hgbv7'
    # Access token secret
    access_token_secret = 'lms33b0Z4Nv6sIKByEf96FYsq3hLDSq1zDsKNSEmb6dCz'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    c = tweepy.Cursor(api.followers_ids, user_id)

    f = open(filename, 'w')
    count = 0
    for follower in c.items():
        count += 1
        f.write(str(follower) + '\n')
    f.close

    print(user_id + ' has ' + str(count) + ' followers.')


def edit_rt(original_filename: str, export_filename: str):
    """get_rtで作ったファイル(original_filename)を処理して不要な情報を取り除き、export_filenameに保存する。

    Args:
        original_filename (str): 元ファイル名
        export_filename (str): 書き出し先ファイル名

    Raises:
        Exception: "original_filename"はcsvファイルである必要があります。
        Exception: "export_filename"はcsvファイルである必要があります。
    """
    if original_filename.endswith('.csv'):
        raise Exception('"original_filename" is not a csv file!')
    if export_filename.endswith('.csv'):
        raise Exception('"export_filename" is not a csv file!')

    df = pd.read_csv(original_filename + '.csv')
    df.drop(columns=['ユーザー名', 'ツイート'], inplace=True)
    print(df)

    df.to_csv(export_filename, index=False)


def connect_rt_follower(
        user_id: str,
        rt_filename: str,
        follower_filename: str,
        export_filename: str):
    """RTのリストについて、それぞれフォロワーであるかを調べる。

    Args:
        user_id (str): ユーザーID
        rt_filename (str): get_rtで作成したファイルのファイル名
        follower_filename (str): get_followerで作成したファイルのファイル名
        export_filename (str): 結果を保存するファイル名

    Raises:
        Exception: "rt_filename"はcsvファイルである必要があります。
        Exception: "follower_filename"はtxtファイルである必要があります。
        Exception: "export_filename"はcsvファイルである必要があります。
    """

    if user_id.startswith('@'):
        user_id = user_id.lstrip('@')

    if rt_filename.endswith('.csv'):
        raise Exception('"rt_filename" is not a csv file!')
    if follower_filename.endswith('.txt'):
        raise Exception('"follower_filename" is not a txt file!')
    if export_filename.endswith('.csv'):
        raise Exception('"export_filename" is not a csv file!')

    # リツイート
    df_RT = pd.read_csv(rt_filename)
    RT_ids = df_RT['ユーザーID'].values.tolist()

    # フォロワー
    f = open(follower_filename)
    follower_ids = []
    line = f.readline().strip()
    while line:
        # print(line.strip())
        follower_ids.append(line)
        line = f.readline().strip()
    f.close

    # フォロワーかどうかを保存するリスト
    follower_in_RT_ids = []
    # リストを0(false)で初期化
    for i in range(len(RT_ids)):
        follower_in_RT_ids.append(0)

    i = 0
    for RT_id in RT_ids:
        # フォロワーなら1
        if str(RT_id) in follower_ids:
            follower_in_RT_ids[i] = 1
        i += 1

    connected_df = pd.DataFrame({
        'userid': RT_ids,
        'follower': follower_in_RT_ids
    })

    connected_df.to_csv(export_filename, index=False)
