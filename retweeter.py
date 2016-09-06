from twython import Twython, TwythonError
import time, re

#get twitter api keys here: https://apps.twitter.com/ .
APP_KEY = 'CONSUMER KEY'
APP_SECRET = 'CONSUMER SECRET'
OAUTH_TOKEN = 'ACCESS TOKEN'
OAUTH_TOKEN_SECRET = 'ACCESS TOKEN SECRET'

HASHTAG = 'gaming' #temporary hashtag
HASHTAG_CREATOR = 'trendsetter_username' #username of trend setter
SEARCH_FILTER = " -".join([" -RT"])

RETWEET_INTERVAL = 36 #delay of retweet in seconds

	
def do_retweet(rt_id,rt_uname,rt_text):
	txt_rt = rt_text.encode('ascii', 'ignore')
	print '[RT] %s : %s' % (rt_uname,txt_rt)
	twitter.retweet(id=rt_id)

def print_hashtag(hashtag):
	print '[HT] %s' % hashtag

def get_hashtag(trend_setter):
	global HASHTAG
	user_ht = None
	print 'checking %s hashtag' % trend_setter
	#look for the last tweet of trend setter
	user_tl = twitter.get_user_timeline(screen_name=trend_setter, count=1,include_rts=False)
	#look for hashtag
	for tweet in user_tl:
		tmp_ht = tweet['entities']['hashtags']
		for ht in tmp_ht:
			user_ht = ht['text']
			#look for keyword. change showtime to anything you want
			tags = re.search(r'showtime', user_ht, re.I)
			if user_ht == HASHTAG:	#old hashtag found
				print_hashtag(user_ht)
				return HASHTAG
			if tags: #new hashtag found using a keyword
				HASHTAG = user_ht
				print_hashtag(HASHTAG)
				return HASHTAG
	if user_ht: #new hashtag
		HASHTAG = user_ht
	print_hashtag(HASHTAG)
	return HASHTAG

def main():
	while True:	
		try:
			SEARCH_TAG = get_hashtag(HASHTAG_CREATOR) + SEARCH_FILTER #get the hashtag
			print "Searching: %s" % SEARCH_TAG
			search_results = twitter.search(q=SEARCH_TAG, count=10) #look for the top 10 unique latest tweet in the hashtag
			#retweet the last 10 post found in search_results. Interval=RETWEET_INTERVAL
			for tweet in search_results["statuses"]:
				do_retweet(tweet['id_str'], tweet['user']['screen_name'],tweet['text'])
				time.sleep(RETWEET_INTERVAL)
		except TwythonError as e:
			print e
		time.sleep(5)

if __name__ == '__main__':
	twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
	main()


