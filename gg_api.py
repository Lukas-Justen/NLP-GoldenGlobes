'''Version 0.35'''
import json
import resources
import pandas as pd

from info_extractor import InfoExtractor
from find_categories import Chunker
from resources import wikidata, EXTERNAL_SOURCES, OFFICIAL_AWARDS_1315, STOPWORDS, OFFICIAL_AWARDS_1819
from tweet_categorizer import TweetCategorizer


def get_hosts(year):
    with open("results.json") as f:
        results = json.load(f)
        print(results[year]["Hosts"])
    return results[year]["Hosts"]


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
    for year in resources.years:
        try:
            extractor = InfoExtractor()
            extractor.load_save("", year, "dirty_gg%s.csv", 500000)
            print("Done loading tweets for " + str(year) + " ...")
        except:
            print("Unable to load tweets for " + str(year) + " ...")
    print("Done Tweets\n")
    return


def main():
    # Reload the csv files from disk and store the data in a dataframe
    # TODO: REMOVE THIS
    resources.years = [2013]
    results = {}

    # Load the csv files and clean data
    print("Load Dataframes")
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
        extractor.drop_column("id")
        extractor.drop_column("timestamp_ms")
        extractor.drop_column("language")
        resources.data[year] = extractor.get_dataframe()
        print("Done loading and cleaning " + str(year) + " dataframe ...")
        results[year] = {}
    print("Done Dataframes\n")

    # We start by finding the awards for each year
    print("Find Awards")
    for year in resources.years:
         chunker = Chunker()
         categorie_data = resources.data[year].copy()
         categorie_data['categorie'] = categorie_data.apply(chunker.extract_wrapper, axis=1)
         categorie_data = categorie_data.loc[categorie_data.categorie != 'N/a', :]
         categorie_data.reset_index(drop=True, inplace=True)
         categorie_data = categorie_data.loc[categorie_data.categorie.str.split().map(len) > 3, :]
         best_categories = chunker.pick_categories(categorie_data)
         best_categories = chunker.filter_categories(best_categories)
         print(best_categories)

    print("Done Awards")

    # Load the wikidata from disk
    people = wikidata.call_wikidate('actors', 'actorLabel') + wikidata.call_wikidate('directors', 'directorLabel')
    people.append("Joanne Frogatte")
    things = wikidata.call_wikidate('films', 'filmLabel') + wikidata.call_wikidate('series', 'seriesLabel')
    things.append("Transparent")
    things.append("Brave")

    # We search for the hosts
    print("Find Hosts")
    for year in resources.years:
        host_categorizer = TweetCategorizer([resources.HOST_WORDS], [], "host_tweet", resources.data[year], 0, 200000)
        host_tweets = host_categorizer.get_categorized_tweets()
        hosters = host_categorizer.find_list_of_entities(host_tweets, 2, people, [])
        results[year]["Hosts"] = hosters[resources.HOST_WORDS]
    print("Done Hosts")

    # Search for the winners
    print("Find Winners")
    for year in resources.years:
        awards = OFFICIAL_AWARDS_1315
        if year in [2018, 2019]:
            awards = OFFICIAL_AWARDS_1819
        winner_categorizer = TweetCategorizer(awards, STOPWORDS, "award", resources.data[year], 3, 1000000)
        winner_tweets = winner_categorizer.get_categorized_tweets()
        winners = winner_categorizer.find_list_of_entities(winner_tweets, 1, people, things)
        for key in winners:
            results[year][key] = {}
            results[year][key]["Winner"] = winners[key]
    print("Done Winners")

    # Save the final results to disk
    with open("results.json", "w") as f:
        json.dump(results, f)
    return


if __name__ == '__main__':
    main()
