import tweepy

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

user_id = 'RazerJP'

c = tweepy.Cursor(api.followers_ids, user_id)

f = open('follower.'+user_id+'.txt', 'w')
count = 0
for follower in c.items():
    count += 1
    print(follower)
    f.write(str(follower)+'\n')

f.close

print(user_id + ' has ' + str(count) + ' followers.')
