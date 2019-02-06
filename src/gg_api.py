'''Version 0.3'''
import pandas as pd

from src.award_winner import TweetCategorizer

OFFICIAL_AWARDS = ['cecil b. demille award',
                   'best motion picture - drama',
                   'best director - motion picture',
                   'best screenplay - motion picture',
                   'best television series - drama',
                   'best motion picture - comedy or musical',
                   'best original song - motion picture',
                   'best foreign language film',
                   'best television series - comedy or musical',
                   'best animated feature film',

                   'best performance by an actress in a motion picture - drama',
                   'best performance by an actor in a motion picture - drama',
                   'best performance by an actress in a motion picture - comedy or musical',
                   'best performance by an actor in a motion picture - comedy or musical',
                   'best performance by an actress in a supporting role in a motion picture',
                   'best performance by an actor in a supporting role in a motion picture',
                   'best original score - motion picture',
                   'best performance by an actress in a television series - drama',
                   'best performance by an actor in a television series - drama',
                   'best performance by an actress in a television series - comedy or musical',
                   'best performance by an actor in a television series - comedy or musical',
                   'best mini-series or motion picture made for television',
                   'best performance by an actress in a mini-series or motion picture made for television',
                   'best performance by an actor in a mini-series or motion picture made for television',
                   'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television',
                   'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']


def get_hosts(year):
    # TODO: Load correct data here
    data = pd.read_csv("../data/cleaned_gg%s.csv" % year)
    host_keywords = "host|hosting|hoster|hosts|anchor|entertainer|entertaining|moderator|moderating|moderated"
    host_categorizer = TweetCategorizer([host_keywords], [], "category", data, 0, 1500000)
    host_tweets = host_categorizer.get_categorized_tweets()
    hosters = host_categorizer.find_list_of_entities(host_tweets, 2)
    return hosters[host_keywords]


def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    awards = ['best motion picture drama',
              'best director motion picture',
              'best screenplay motion picture',
              'best television series drama',
              'best motion picture musical or comedy',
              'best original song motion picture',
              'best foreign language film',
              'best television series comedy or musical',
              'best motion picture comedy or musical',
              'best animated feature film',

              # 'best tv series comedy',
              # 'best television series actor',
              # 'best actor tv series',
              ]
    return awards


def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    nominees = []
    return nominees


def get_winner(year):
    # TODO: Load correct data here
    data = pd.read_csv("../data/cleaned_gg%s.csv" % year)
    stopwords = ["an", "in", "a", "for", "by", "-", "or"]
    award_categorizer = TweetCategorizer(OFFICIAL_AWARDS, stopwords, "award", data, 3, 170000)
    award_tweets = award_categorizer.get_categorized_tweets()
    winners = award_categorizer.find_frequent_entity(award_tweets)
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
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    return


if __name__ == '__main__':
    main()
