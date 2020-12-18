import pandas as pd
filename = 'retweet_info@goando'

df = pd.read_csv(filename+'.csv')
df.drop(columns=['ユーザー名', 'ツイート'], inplace=True)
print(df)

df.to_csv(filename+'.edited.csv', index=False)
