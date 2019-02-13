'''Version 0.3'''
import pandas as pd

from src.tweet_categorizer import TweetCategorizer
from src.wikidata_connector import WikidataConnector

OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama',
                   'best performance by an actress in a motion picture - drama',
                   'best performance by an actor in a motion picture - drama',
                   'best motion picture - comedy or musical',
                   'best performance by an actress in a motion picture - comedy or musical',
                   'best performance by an actor in a motion picture - comedy or musical',
                   'best animated feature film', 'best foreign language film',
                   'best performance by an actress in a supporting role in a motion picture',
                   'best performance by an actor in a supporting role in a motion picture',
                   'best director - motion picture', 'best screenplay - motion picture',
                   'best original score - motion picture', 'best original song - motion picture',
                   'best television series - drama',
                   'best performance by an actress in a television series - drama',
                   'best performance by an actor in a television series - drama',
                   'best television series - comedy or musical',
                   'best performance by an actress in a television series - comedy or musical',
                   'best performance by an actor in a television series - comedy or musical',
                   'best mini-series or motion picture made for television',
                   'best performance by an actress in a mini-series or motion picture made for television',
                   'best performance by an actor in a mini-series or motion picture made for television',
                   'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television',
                   'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']


def get_hosts(year):
    data = pd.read_csv("../data/cleaned_gg%s.csv" % year)
    print("Wikidata")
    wikidata = WikidataConnector()
    actors = wikidata.call_wikidate("actors", 'actorLabel')
    directors = wikidata.call_wikidate("directors", 'directorLabel')

    print("Categorizer")
    host_keywords = "host|hosting|hoster|hosts|anchor|entertainer|entertaining|moderator|moderating|moderated"
    host_categorizer = TweetCategorizer([host_keywords], [], "category", data, 0, 1000000)
    host_tweets = host_categorizer.get_categorized_tweets()
    hosters = host_categorizer.find_list_of_entities(host_tweets, 2, actors + directors, [])
    return hosters[host_keywords]


def get_awards(year):
    return []


def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    nominees = []
    return nominees


def get_winner(year):
    data = pd.read_csv("../data/cleaned_gg%s.csv" % year)
    stopwords = ["an", "in", "a", "for", "by", "-", "or"]
    print("Wikidata")
    wikidata = WikidataConnector()
    actors = wikidata.call_wikidate("actors", 'actorLabel')
    films = wikidata.call_wikidate("films", 'filmLabel')
    series = wikidata.call_wikidate("series", 'seriesLabel')
    directors = wikidata.call_wikidate("directors", 'directorLabel')
    print(len(actors))
    print(len(films))
    print(len(directors))
    print(len(series))
    print("Categorizer")
    winner_categorizer = TweetCategorizer(OFFICIAL_AWARDS, stopwords, "award", data, 3, 1000000)
    winner_tweets = winner_categorizer.get_categorized_tweets()
    winners = winner_categorizer.find_list_of_entities(winner_tweets, 1, actors + directors, films + series)
    winner_categorizer.print_frequent_entities()
    return winners


def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    presenters = []
    return presenters


def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    print("Pre-ceremony processing complete.")
    return


def main():
    '''This function calls your program. Typing "python gg_api_old.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    return


if __name__ == '__main__':
    main()
