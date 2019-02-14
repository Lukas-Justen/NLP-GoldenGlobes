from tweet_categorizer import TweetCategorizer

# TODO: Remove the visualization tasks for the final submission
# extractor.count_words_per_tweet("text")
# extractor.count_words_per_tweet("clean_text")
# visualizer_old = DataVisualizer(extractor.get_dataframe(), "text")
# visualizer_new = DataVisualizer(extractor.get_dataframe(), "clean_text")
# visualizer_old.show_analysis()
# visualizer_new.show_analysis()

# TODO: Remove these lines since they are only for here debugging
# extractor = InfoExtractor()
# extractor.read_dataframe("../data/cleaned_gg%s.csv" % kb_constant.year)
# data = extractor.get_dataframe()


print("HALLLO")

# HOSTS
# host_categorizer = TweetCategorizer([host_keywords], [], "host_tweet", data, 0, 1700000)
# host_tweets = host_categorizer.get_categorized_tweets()
# print(len(host_tweets))
# hosters = host_categorizer.find_list_of_entities(host_tweets, 10, actors)
# print(hosters)

# WINNERS
# winner_categorizer = TweetCategorizer(awards, stopwords, "award", data, 3, 1000000)
# winner_tweets = winner_categorizer.get_categorized_tweets()
# winners = winner_categorizer.find_list_of_entities(winner_tweets, 1, actors + directors, films + series)
# winner_categorizer.print_frequent_entities()

# # TIMES
# award_categorizer = TweetCategorizer(kb_constant.awards, kb_constant.stopwords, "award", data, 3, 1500000)
# award_tweets = award_categorizer.get_categorized_tweets()
# award_tweets["absolute_time"] = award_tweets["hour"].apply(lambda hour: hour * 60)
# award_tweets["absolute_time"] += award_tweets["minute"].apply(lambda minute: minute)
# average_time = award_tweets.groupby(['award']).mean()
# average_time = average_time.sort_values(by=["absolute_time", "hour", "minute"])
#
# # NOMINEES
# nominee_categorizer = TweetCategorizer([kb_constant.nominee_keywords], [], "category", data, 0, 1500000)
# nominee_tweets = nominee_categorizer.get_categorized_tweets()
# nominees = nominee_categorizer.find_list_of_entities(nominee_tweets, 200)
#
# # PRESENTER
# presenter_categorizer = TweetCategorizer([kb_constant.presenter_keywords], [], "category", data, 0, 1500000)
# presenter_tweets = presenter_categorizer.get_categorized_tweets()
# presenter_tweets = presenter_tweets.sort_values(by=["hour", "minute"])
# presenter_pattern = []
# presenter_pattern.append(re.compile(r'([A-Z][a-zA-Z]* [A-Z][a-zA-Z]*) ([A-Z][a-zA-Z]* [A-Z][a-zA-Z]*) present'))
# presenter_pattern.append(re.compile(r'[a-z]+ ([A-Z][a-zA-Z]* [A-Z][a-zA-Z]* [A-Z][a-zA-Z]*) presents'))
# presenter_pattern.append(re.compile(r'[a-z]+ [a-z]+ ([A-Z][a-zA-Z]* [A-Z][a-zA-Z]*) presents'))
# for index, row in presenter_tweets.iterrows():
#     for p in presenter_pattern:
#         matches = p.findall(row['clean_text'])
#         for m in matches:
#             print(m)
