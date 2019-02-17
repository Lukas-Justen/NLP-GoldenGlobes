'''Version 0.35'''
import json
import urllib.request
import urllib.parse
import re

from google_images_download import google_images_download

import resources
from info_extractor import InfoExtractor
from resources import wikidata, EXTERNAL_SOURCES
from tweet_categorizer import TweetCategorizer


def get_hosts(year):
    with open("results.json") as f:
        results = json.load(f)
    hosts = results[year]["Hosts"]
    return hosts


def get_awards(year):
    with open("results.json") as f:
        results = json.load(f)
        awards = results[year]["Awards"]
    return awards


def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    nominees = []
    return nominees


def get_winner(year):
    awards = resources.OFFICIAL_AWARDS_1315
    if year in [2018, 2019]:
        awards = resources.OFFICIAL_AWARDS_1819
    with open("results.json") as f:
        results = json.load(f)
    winners = {}
    for key in awards:
        winners[key] = results[year][key]["Winner"]
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
    all_winners = {}

    # Load the csv files and clean data
    print("Load Dataframes")
    for year in resources.years:
        extractor = InfoExtractor()
        print("Start " + str(year) + " ...")
        print("Reading ...")
        extractor.read_dataframe("dirty_gg%s.csv" % year)
        print("Language ...")
        extractor.get_english_tweets("text", "language")
        print("Cleaning ...")
        extractor.clean_dataframe_column("text", "clean_upper")
        print("Lowering ...")
        extractor.make_to_lowercase("clean_upper", "clean_lower")
        print("Droping ...")
        extractor.drop_column("user")
        extractor.drop_column("id")
        extractor.drop_column("timestamp_ms")
        extractor.drop_column("language")
        resources.data[year] = extractor.get_dataframe()
        print("Finish " + str(year) + " ...")
        results[year] = {}
    print("Done Dataframes\n")

    # # We start by finding the awards for each year
    # print("Find Awards")
    # for year in resources.years:
    #     chunker = Chunker()
    #     categorie_data = resources.data[year].copy()
    #     categorie_data['categorie'] = categorie_data.apply(chunker.extract_wrapper, axis=1)
    #     categorie_data = categorie_data.loc[categorie_data.categorie != 'N/a', :]
    #     categorie_data.reset_index(drop=True, inplace=True)
    #     categorie_data = categorie_data.loc[categorie_data.categorie.str.split().map(len) > 3, :]
    #     best_categories = chunker.pick_categories(categorie_data)
    #     best_categories = chunker.filter_categories(best_categories)
    #     results[year]["Awards"] = best_categories
    # print("Done Awards\n")
    #
    # # Load the wikidata from disk
    people = wikidata.call_wikidate('actors', 'actorLabel') + wikidata.call_wikidate('directors', 'directorLabel')
    # things = wikidata.call_wikidate('films', 'filmLabel') + wikidata.call_wikidate('series', 'seriesLabel')
    #
    # # We search for the hosts
    # print("Find Hosts")
    # for year in resources.years:
    #     host_categorizer = TweetCategorizer([resources.HOST_WORDS], [], "host_tweet", resources.data[year], 0, 200000)
    #     host_tweets = host_categorizer.get_categorized_tweets()
    #     hosters = host_categorizer.find_percentage_of_entities(host_tweets, 0.2, people, [])
    #     results[year]["Hosts"] = hosters[resources.HOST_WORDS]
    # print("Done Hosts\n")
    #
    # # Search for the winners
    # print("Find Winners")
    # for year in resources.years:
    #     all_winners[year] = []
    #     awards = resources.OFFICIAL_AWARDS_1315
    #     if year in [2018, 2019]:
    #         awards = resources.OFFICIAL_AWARDS_1819
    #     winner_categorizer = TweetCategorizer(awards, resources.STOPWORDS, "award", resources.data[year], 3, 1000000)
    #     winner_tweets = winner_categorizer.get_categorized_tweets()
    #     winners = winner_categorizer.find_list_of_entities(winner_tweets, 1, people, things)
    #     for key in winners:
    #         results[year][key] = {}
    #         results[year][key]["Winner"] = winners[key]
    #         all_winners[year].append(winners[key])
    # print("Done Winners\n")

    # Search for best and worst dress
    # print("Find Dresses")
    # for year in resources.years:
    #     dress_categorizer = TweetCategorizer([resources.DRESS], [], "dress", resources.data[year], 0,
    #                                          resources.data[year].shape[0])
    #     dress_tweets = dress_categorizer.get_categorized_tweets()
    #
    #     best_dress_categorizer = TweetCategorizer([resources.BEST_DRESS], [], "best_dress", dress_tweets, 0,
    #                                               dress_tweets.shape[0])
    #     best_dress_tweets = best_dress_categorizer.get_categorized_tweets()
    #     probs_best = best_dress_categorizer.list_probabilities(best_dress_tweets, 3, people, [], people=True)
    #     best_dressed = list(probs_best.keys())
    #     representative_best_tweets = []
    #     for b in best_dressed:
    #         for index, row in best_dress_tweets.iterrows():
    #             if b in str(row["clean_upper"]):
    #                 representative_best_tweets.append(str(row["text"]))
    #                 break
    #
    #     worst_dress_categorizer = TweetCategorizer([resources.WORST_DRESS], [], "worst_dress", dress_tweets, 0,
    #                                                dress_tweets.shape[0])
    #     worst_dress_tweets = worst_dress_categorizer.get_categorized_tweets()
    #     probs_worst = worst_dress_categorizer.list_probabilities(worst_dress_tweets, 3, people, [], people=True)
    #     worst_dressed = list(probs_worst.keys())
    #
    #     representative_worst_tweets = []
    #     for w in worst_dressed:
    #         for index, row in worst_dress_tweets.iterrows():
    #             if w in str(row["clean_upper"]):
    #                 representative_worst_tweets.append(str(row["text"]))
    #                 break
    #
    #     results[year]["BestDressed"] = probs_best
    #     results[year]["WorstDressed"] = probs_worst
    #     results[year]["BestDressedTweets"] = representative_best_tweets
    #     results[year]["WorstDressedTweets"] = representative_worst_tweets
    # print("Done Dresses\n")

    # Search for best and worst dress
    print("Find Jokes")
    for year in resources.years:
        # joke_categorizer = TweetCategorizer([resources.JOKES], [], "jokes", resources.data[year], 0, resources.data[year].shape[0])
        # joke_tweets = joke_categorizer.get_categorized_tweets()
        # funny_people = joke_categorizer.find_list_of_entities(joke_tweets, 5, people, [], people=True)[resources.JOKES]
        # representative_joke_tweets = []
        # for f in funny_people:
        #     for index, row in joke_tweets.iterrows():
        #         if f in str(row["clean_lower"]):
        #             representative_joke_tweets.append(str(row["text"]))
        #             break
        # results[year]["JokeTweets"] = representative_joke_tweets
        # results[year]["FunnyPeople"] = funny_people

        moment_categorizer = TweetCategorizer([resources.MOMENTS], [], "moments", resources.data[year], 0, resources.data[year].shape[0])
        moment_tweets = moment_categorizer.get_categorized_tweets()
        link_finder = re.compile(r'http(s)?\:\/\/[\w\.\d]*\b')
        results[year]["Moments"] = {}
        for type in resources.MOMENT_TYPES:
            type_categorizer = TweetCategorizer([type], [], "jokes", moment_tweets, 0, moment_tweets.shape[0])
            type_tweets = type_categorizer.get_categorized_tweets()
            type_people = type_categorizer.find_list_of_entities(type_tweets, 1, people, [], people=True)[type]
            results[year]["Moments"][type] = {}
            results[year]["Moments"][type]["Person"] = type_people
            for index, row in type_tweets.iterrows():
                if type_people in str(row["clean_lower"]):
                    results[year]["Moments"][type]["Tweet"] = str(row["text"])
                    break
            http_categorizer = TweetCategorizer(["http"], [], "links", type_tweets, 0, type_tweets.shape[0],column="text")
            http_tweets = http_categorizer.get_categorized_tweets()
            print(str(http_tweets["text"][0]))
            link = link_finder.findall(str(http_tweets["text"][0]))
            results[year]["Moments"][type]["Link"] = link
    print("Done Jokes\n")

    markdown = ""
    for year in resources.years:
        markdown += "# " + str(year) + " Golden Globes\n"
        # markdown += "##### Hosts\n"
        # for h in results[year]["Hosts"]:
        #     markdown += " - " + h + "\n"

        # markdown += "##### Awards\n"
        # for a in results[year]["Awards"]:
        #     markdown += " - " + a + "\n"

        markdown += "##### Best Dressed\n"
        i = 0
        best_dressed = list(results[year]["BestDressed"].keys())
        for b in best_dressed:
            markdown += " " + str(i) + ". " + b + " (" + str(results[year]["BestDressed"][b]) + ") " + "\n"
            i += 1
        markdown += "\n"
        for b in best_dressed:
            response = google_images_download.googleimagesdownload()
            search = b + " " + str(year) + " Golden Globes Dress"
            arguments = {"keywords": search, "limit": 1, "print_urls": False}
            paths = response.download(arguments)
            markdown += "<img src='file://" + paths[search][0] + "' height=300px alt='" + search + "'>  "
        markdown += "\n"
        markdown += "\n"
        for b in results[year]["BestDressedTweets"]:
            markdown += b + "  \n\n"
        markdown += "\n"

        markdown += "##### Worst Dressed\n"
        i = 0
        worst_dressed = list(results[year]["WorstDressed"].keys())
        for w in worst_dressed:
            markdown += " " + str(i) + ". " + w + " (" + str(results[year]["WorstDressed"][w]) + ") " + "\n"
            i += 1

        markdown += "\n"
        for w in worst_dressed:
            response = google_images_download.googleimagesdownload()
            search = w + " " + str(year) + " Golden Globes Dress"
            arguments = {"keywords": search, "limit": 1, "print_urls": False}
            paths = response.download(arguments)
            markdown += "<img src='file://" + paths[search][0] + "' height=300px alt='" + search + "'>  "
        markdown += "\n"
        markdown += "\n"
        for w in results[year]["WorstDressedTweets"]:
            markdown += w + "  \n\n"
        markdown += "\n"

        # print("Find Presenters")
        # for year in resources.years:
        #
        #     if year in [2013, 2015]:
        #         awards = OFFICIAL_AWARDS_1315
        #     else:
        #         awards = OFFICIAL_AWARDS_1819
        #
        #     temp_list = []
        #     for each_award in awards:
        #         temp_list.append(each_award + " " + results[year][each_award]["Winner"])
        #
        #     presenter_categorizer = TweetCategorizer([resources.PRESENTER_WORDS], [], "presenter_tweet",
        #                                              resources.data[year], 0, resources.data[year].shape[0])
        #     presenter_tweets = presenter_categorizer.get_categorized_tweets()
        #     presenter = presenter_categorizer.find_list_of_entities(presenter_tweets, 70, people, [], people=True)[
        #         resources.PRESENTER_WORDS]
        #     print(presenter)
        #     presenter = [p for p in presenter if p not in all_winners[year] and p not in results[year]["Hosts"]]
        #     print(presenter)
        #
        #     nominee_categorizer = TweetCategorizer([resources.NOMINEE_WORDS], [], "nominee_tweet", resources.data[year], 0,
        #                                            resources.data[year].shape[0])
        #     nominee_tweets = nominee_categorizer.get_categorized_tweets()
        #     nominees = nominee_categorizer.find_list_of_entities(nominee_tweets, 150, people + things, [], people=True)[
        #         resources.NOMINEE_WORDS]
        #     print(nominees)
        #     nominees = [p for p in nominees if p not in all_winners[year] and p not in results[year]["Hosts"]]
        #     print(nominees)
        #
        #     presenters_dict = {}
        #     for each_award in awards:
        #         each_award = each_award + " " + results[year][each_award]["Winner"]
        #         each_award = each_award.split()
        #
        #         each_award = [each_ for each_ in each_award if not each_ == '-' and len(each_) > 2]
        #
        #         format_award = '|'.join(each_award)
        #
        #         award_categorizer = TweetCategorizer([format_award], [], "specific_award_tweet", presenter_tweets, 3, presenter_tweets.shape[0])
        #         award_tweets = award_categorizer.get_categorized_tweets()
        #
        #         presenters = award_categorizer.find_list_of_entities(award_tweets, 2, people, [], people=True)
        #
        #         each_award = ' '.join(each_award)
        #         presenters_dict[each_award] = presenters[format_award]
        #         print(each_award, ' - ', presenters[format_award])

    # Save the final results to disk
    with open('results.md', 'w') as file:
        file.write(markdown)

    with open("results.json", "w") as f:
        json.dump(results, f)
    return


if __name__ == '__main__':
    main()
