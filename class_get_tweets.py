import tweepy
from termcolor import colored

class TweetRepo:
 
    def __init__(self):
        # Consumer keys and access tokens, used for OAuth
        consumer_key = '4TKNNrgQZiYN9OILjYapJbNsG'
        consumer_secret = 'dRFBEVNhs66MhXoHsieJJpim6R3DR3yOdkwhZBod4r7OcgP5yH'
        access_token = '254482168-zF8sGt7vX82qaQSGaXMv5qSiG48IS7RuVvkRzTHB'
        access_token_secret = 'CK5x281qRnIYtvlLZiz0GazGBpKeWHPVIqCdowuyLv3mh'
 
        # OAuth process, using the keys and tokens
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
        self.region = 'world_wide'

    def set_region(self,region_name):
        self.region = region_name

    def write_tweets_to_file(self,f):
        place_to_woeid = {'world_wide' : 1, 'bengaluru' : 2295420, 'india' : 23424848}
        trends_info = self.api.trends_place(place_to_woeid[self.region])[0]['trends']

        print 'The current trends :'
        for trend_info in trends_info:
            print trend_info['name']

        print 'Collecting tweets from the first hashtag %s'%trends_info[0]['name']
        c = tweepy.Cursor(self.api.search, q=trends_info[0]['name'], include_entities=True)

        tweet_list = []

        for tweet in c.items(100):
            #tweet_list.append(tweet.text.encode('UTF-8').replace('\n',' '))
            tweet_list.append(tweet.text.encode('UTF-8').replace('\n','\n\n'))

        for tweet in tweet_list:
            f.write(tweet)
            f.write('%%')

    def search_relevant_tweets(self, search_string, limit=50):
        print
        print 'The search is for %s'%(colored(search_string, 'cyan'))
        results = self.api.search(q=search_string, lang='en', count=limit,show_user=True)
        print
        print colored('Number of results for the search %s is %s'%(repr(search_string),repr((str(len(results))))), 'magenta')

        for result in results:
            print
            print colored(result.text, 'red') + ' - ' + result.user.name + ' - ' + '@' + colored(result.user.screen_name, 'green')
