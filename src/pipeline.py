from src.info_extractor import InfoExtractor
from src.tweet_categorizer import TweetCategorizer
from src.wikidata_connector import WikidataConnector

year = 2013

awards = ['cecil b. demille award', 'best performance by an actress in a supporting role in a motion picture',
          'best motion picture - drama', 'best performance by an actor in a television series - comedy or musical',
          'best director - motion picture', 'best performance by an actor in a supporting role in a motion picture',
          'best screenplay - motion picture', 'best mini-series or motion picture made for television',
          'best television series - drama', 'best performance by an actress in a television series - comedy or musical',
          'best motion picture - comedy or musical', 'best original song - motion picture',
          'best foreign language film', 'best television series - comedy or musical', 'best animated feature film',
          'best performance by an actress in a motion picture - drama',
          'best performance by an actor in a motion picture - drama', 'best original score - motion picture',
          'best performance by an actress in a motion picture - comedy or musical',
          'best performance by an actor in a motion picture - comedy or musical',
          'best performance by an actress in a television series - drama',
          'best performance by an actor in a television series - drama',
          'best performance by an actress in a mini-series or motion picture made for television',
          'best performance by an actor in a mini-series or motion picture made for television',
          'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television',
          'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
host_keywords = "host|hosting|hoster|hosts|anchor|entertainer|entertaining|moderator|moderating|moderated|entertained"
nominee_keywords = "nominee|nomination|nominated|nominees|nominations|nominate|vote|voting|voter|voted|candidate"
presenter_keywords = "present|presents|presenting|presented|presentation|presenter|presenters|presentations|introduce"
stopwords = ["an", "in", "a", "for", "by", "-", "or"]

# TODO: This code has to be uncommented for the final submission
# extractor = InfoExtractor()
# extractor.load_data("../data/", year)
# extractor.clean_dataframe_column("text", "clean_text")
# extractor.convert_time("timestamp_ms")
# extractor.drop_column("user")
# extractor.drop_column("id")
# extractor.drop_column("timestamp_ms")
# extractor.save_dataframe("../data/cleaned_gg%s.csv" %year)
# data = extractor.get_dataframe()

# TODO: Remove the visualization tasks for the final submission
# extractor.count_words_per_tweet("text")
# extractor.count_words_per_tweet("clean_text")
# visualizer_old = DataVisualizer(extractor.get_dataframe(), "text")
# visualizer_new = DataVisualizer(extractor.get_dataframe(), "clean_text")
# visualizer_old.show_analysis()
# visualizer_new.show_analysis()

# TODO: Remove these lines since they are only for here debugging
extractor = InfoExtractor()
extractor.read_dataframe("../data/cleaned_gg%s.csv" % year)
data = extractor.get_dataframe()

wikidata = WikidataConnector()
actors = wikidata.call_wikidate('actors', 'actorLabel')
films = wikidata.call_wikidate('films', 'filmLabel')
series = wikidata.call_wikidate('directors', 'directorLabel')
directors = wikidata.call_wikidate('series', 'seriesLabel')
films.append("Transparent")
actors.append("Brave")
actors.append("Joanne Frogatte")

# HOSTS
# host_categorizer = TweetCategorizer([host_keywords], [], "host_tweet", data, 0, 1700000)
# host_tweets = host_categorizer.get_categorized_tweets()
# print(len(host_tweets))
# hosters = host_categorizer.find_list_of_entities(host_tweets, 10, actors)
# print(hosters)

# WINNERS
winner_categorizer = TweetCategorizer(awards, stopwords, "award", data, 3, 1000000)
winner_tweets = winner_categorizer.get_categorized_tweets()
winners = winner_categorizer.find_list_of_entities(winner_tweets, 1, actors + directors, films + series)
winner_categorizer.print_frequent_entities()

# # TIMES
# award_categorizer = TweetCategorizer(awards, stopwords, "award", data, 3, 1500000)
# award_tweets = award_categorizer.get_categorized_tweets()
# award_tweets["absolute_time"] = award_tweets["hour"].apply(lambda hour: hour * 60)
# award_tweets["absolute_time"] += award_tweets["minute"].apply(lambda minute: minute)
# average_time = award_tweets.groupby(['award']).mean()
# average_time = average_time.sort_values(by=["absolute_time", "hour", "minute"])
#
# # NOMINEES
# nominee_categorizer = TweetCategorizer([nominee_keywords], [], "category", data, 0, 1500000)
# nominee_tweets = nominee_categorizer.get_categorized_tweets()
# nominees = nominee_categorizer.find_list_of_entities(nominee_tweets, 200)
#
# # PRESENTER
# presenter_categorizer = TweetCategorizer([presenter_keywords], [], "category", data, 0, 1500000)
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
