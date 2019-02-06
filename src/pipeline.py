import pandas as pd

from src.award_winner import TweetCategorizer

year = 2013

data = pd.read_csv("../data/cleaned_gg%s.csv" % year)
host_keywords = "host|hosting|hoster|hosts|anchor|entertainer|entertaining|moderator|moderating|moderated"
host_categorizer = TweetCategorizer([host_keywords], [], "category", data, 0, 1500000)
host_tweets = host_categorizer.get_categorized_tweets()
hosters = host_categorizer.find_list_of_entities(host_tweets, 2)
print(hosters[host_keywords])
