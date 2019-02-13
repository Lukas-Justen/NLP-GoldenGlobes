'''Version 0.35'''

from src import resources
from src.info_extractor import InfoExtractor
from src.resources import wikidata, EXTERNAL_SOURCES, OFFICIAL_AWARDS_1315, STOPWORDS
from src.tweet_categorizer import TweetCategorizer


def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    hosts = []
    return hosts


def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    awards = []
    return awards


def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    nominees = []
    return nominees


def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    winners = []
    return winners


def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    presenters = []
    return presenters


def pre_ceremony():
    # Here we load actors, films, directors and series from wikidata
    print("Load Wikidata")
    for key in EXTERNAL_SOURCES:
        wikidata.call_wikidate(key, EXTERNAL_SOURCES[key])
        print("Done loading " + key + " ...")
    print("Done Wikidata\n")

    # Here we load all the zip files and store them in a csv file
    print("Load Tweets")
    remove = []
    for year in resources.years:
        try:
            extractor = InfoExtractor()
            extractor.load_save("", year, "dirty_gg%s.csv", 500000)
            print("Done loading tweets for " + str(year) + " ...")
        except:
            remove.append(year)
            print("Unable to load tweets for " + str(year) + " ...")
    resources.years = [y for y in resources.years if y not in remove]
    print("Done Tweets\n")

    # Done pre-processing now we can start cleaning it
    print("Pre-ceremony processing complete.")
    return


def main():
    # Reload the csv files from disk and store the data in a dataframe
    print("Load Dataframes")
    # TODO: REMOVE THIS
    resources.years = [2013,2015]
    for year in resources.years:
        extractor = InfoExtractor()
        print("Read ...")
        extractor.read_dataframe("dirty_gg%s.csv" % year)
        print("Language ...")
        extractor.get_english_tweets("text", "language")
        print("Cleaning ...")
        extractor.clean_dataframe_column("text", "clean_upper")
        print("Lowering ...")
        extractor.make_to_lowercase("clean_upper", "clean_lower")
        print("Drop ...")
        extractor.drop_column("user")
        print("Drop ...")
        extractor.drop_column("id")
        print("Drop ...")
        extractor.drop_column("timestamp_ms")
        print("Drop ...")
        extractor.drop_column("language")
        resources.data[year] = extractor.get_dataframe()
        print("Done loading and cleaning " + str(year) + " dataframe ...")
    print("Done Dataframes\n")

    # We start by finding the awards for each year
    # print("Find Awards")
    # for year in resources.years:
    #     chunker = Chunker()
    #     resources.data[year]['categorie'] = resources.data[year].apply(chunker.extract_wrapper, axis=1)
    #     resources.data[year] = resources.data[year].loc[resources.data[year]['categorie'] != 'N/a', :]
    #     resources.data[year].reset_index(drop=True, inplace=True)
    #     resources.data[year][['nominee_mentioned', 'presenter_mentioned', 'categorie']] = pd.DataFrame(
    #         resources.data[year]['categorie'].values.tolist(), index=resources.data[year].index)
    #     resources.data[year] = resources.data[year].loc[resources.data[year]['categorie'].str.split().map(len) > 3, :]
    #     found_categories = chunker.pick_categories(resources.data[year])
    #     print(found_categories)
    # print("Done Awards")

    people = wikidata.call_wikidate('actors', 'actorLabel') + wikidata.call_wikidate('directors', 'directorLabel')
    things = wikidata.call_wikidate('films', 'filmLabel') + wikidata.call_wikidate('series', 'seriesLabel')

    # We search for the hosts
    print("Find Hosts")
    for year in resources.years:
        host_categorizer = TweetCategorizer([resources.HOST_WORDS], [], "host_tweet", resources.data[year], 0, 200000)
        host_tweets = host_categorizer.get_categorized_tweets()
        hosters = host_categorizer.find_list_of_entities(host_tweets, 2, people, [])
        print(hosters)
    print("Done Hosts")

    # We search for the hosts
    print("Find Winners")
    for year in resources.years:
        winner_categorizer = TweetCategorizer(OFFICIAL_AWARDS_1315, STOPWORDS, "award", resources.data[year], 3, 1000000)
        winner_tweets = winner_categorizer.get_categorized_tweets()
        winners = winner_categorizer.find_list_of_entities(winner_tweets, 1, people, things)
    print("Done Winners")


    return


if __name__ == '__main__':
    main()
