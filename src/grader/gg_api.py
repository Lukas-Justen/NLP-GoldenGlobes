'''Version 0.35'''
from src.info_extractor import InfoExtractor
from src.wikidata_connector import WikidataConnector

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']
EXTERNAL_SOURCES = {'actors': 'actorLabel', 'films': 'filmLabel', 'directors': 'directorLabel', 'series': 'seriesLabel'}
HOST_WORDS = "host|hosting|hoster|hosts|anchor|entertainer|entertaining|moderator|moderating|moderated|entertained"
NOMINEE_WORDS = "nominee|nomination|nominated|nominees|nominations|nominate|vote|voting|voter|voted|candidate"
PRESENTER_WORDS = "present|presents|presenting|presented|presentation|presenter|presenters|presentations|introduce"
STOPWORDS = ["an", "in", "a", "for", "by", "-", "or"]
YEARS = [2013, 2015, 2018, 2019]

wikidata = WikidataConnector()
extractor = InfoExtractor()
data = {}

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
    for year in YEARS:
        try:
            extractor.load_save("", year, "dirty_gg%s.csv")
            print("Done loading tweets for " + str(year) + " ...")
        except:
            print("Unable to load tweets for " + str(year) + " ...")
    print("Done Tweets\n")

    # Done pre-processing now we can start cleaning it
    print("Pre-ceremony processing complete.")
    return


def main():
    # Reload the csv files from disk and store the data in a dataframe
    print("Load Dataframes")
    for year in YEARS:
        extractor.read_dataframe("dirty_gg%s.csv" % year)
        print("Done loading " + str(year) + " dataframe ...")
    print("Done Dataframes")

    # '''This function calls your program. Typing "python gg_api.py"
    # will run this function. Or, in the interpreter, import gg_api
    # and then run gg_api.main(). This is the second thing the TA will
    # run when grading. Do NOT change the name of this function or
    # what it returns.'''
    # Your code here
    return


if __name__ == '__main__':
    pre_ceremony()
