import pandas as pd
import csv

# 処理するユーザー名
user_name = 'goando'

# リツイート
df_RT = pd.read_csv('retweet_info@'+user_name+'.edited.csv')
RT_ids = df_RT['ユーザーID'].values.tolist()

# フォロワー
f = open('follower.'+user_name+'.txt')
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

print(connected_df)

connected_df.to_csv('./connected.'+user_name+'.csv', index=False)
