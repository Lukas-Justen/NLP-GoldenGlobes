'''Version 0.35'''
from src.constants import EXTERNAL_SOURCES, YEARS
from src.info_extractor import InfoExtractor
from src.wikidata_connector import WikidataConnector

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
        extractor.get_english_tweets()
        extractor.clean_dataframe_column("text", "clean_text")
        extractor.convert_time("timestamp_ms")
        extractor.drop_column("user")
        extractor.drop_column("id")
        extractor.drop_column("timestamp_ms")
        extractor.drop_column("language")
        extractor.save_dataframe("cleaned_gg%s.csv" % year)
        data[year] = extractor.get_dataframe()
        print("Done loading and cleaning " + str(year) + " dataframe ...")
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
