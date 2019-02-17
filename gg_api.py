'''Version 0.35'''
import json
import re

import pandas as pd
from google_images_download import google_images_download

import resources
from find_categories import Chunker
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
    awards = resources.OFFICIAL_AWARDS_1315
    if year in [2018, 2019]:
        awards = resources.OFFICIAL_AWARDS_1819
    with open("results.json") as f:
        results = json.load(f)
    nominees = {}
    for key in awards:
        nominees[key] = results[year][key]["Nominees"]
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
    awards = resources.OFFICIAL_AWARDS_1315
    if year in [2018, 2019]:
        awards = resources.OFFICIAL_AWARDS_1819
    with open("results.json") as f:
        results = json.load(f)
    presenters = {}
    for key in awards:
        presenters[key] = results[year][key]["Presenters"]
    return presenters


def pre_ceremony():
    # Here we load actors, films, directors and series from wikidata
    print("Load Wikidata")
    for key in EXTERNAL_SOURCES:
        if key == "films":
            for year in resources.years:
                wikidata.call_wikidate(key, EXTERNAL_SOURCES[key], str(year - 2), str(year))
        else:
            wikidata.call_wikidate(key, EXTERNAL_SOURCES[key])
        print("Done loading " + key + " ...")
    print("Done Wikidata\n")

    # Here we load all the zip files and store them in a csv file
    print("Load Tweets")
    for year in resources.years:
        try:
            extractor = InfoExtractor()
            extractor.load_save("", year, 300000)
            print("Done loading tweets for " + str(year) + " ...")
        except:
            print("Unable to load tweets for " + str(year) + " ...")
    print("Done Tweets\n")
    return


def fuzz_(ident_catg, awards):
    list_ident = ident_catg.split()
    total_len = len(list_ident)

    best_value_percent = 0
    best_value = ''

    for key, value in awards.items():
        value = value.split()
        count = 0
        for each_ in list_ident:
            if each_ in value:
                count += 1

        if count / total_len > best_value_percent:
            best_value_percent = count / total_len
            best_value = key

    if best_value_percent > 0.4:
        return best_value
    else:
        return 'N/a'


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
        print("Drop ...")

        extractor.convert_time('timestamp_ms')
        extractor.drop_column("user")
        extractor.drop_column("id")
        extractor.drop_column("timestamp_ms")
        extractor.drop_column("language")
        resources.data[year] = extractor.get_dataframe()
        print("Finish " + str(year) + " ...")
        results[year] = {}
    print("Done Dataframes\n")

    # We start by finding the awards for each year
    print("Find Awards")
    categorie_data = {}
    best_catg_time = {}
    clean_awards = {}
    for year in resources.years:
        chunker = Chunker()
        categorie_data[year] = resources.data[year].copy()
        categorie_data[year]['categorie'] = categorie_data[year].apply(chunker.extract_wrapper, axis=1)
        categorie_data[year] = categorie_data[year].loc[categorie_data[year].categorie != 'N/a', :]
        categorie_data[year].reset_index(drop=True, inplace=True)
        categorie_data[year] = categorie_data[year].loc[categorie_data[year].categorie.str.split().map(len) > 3, :]
        best_categories = chunker.pick_categories(categorie_data[year])
        best_categories = chunker.filter_categories(best_categories)
        print(best_categories)
        results[year]["Awards"] = best_categories
    print("Done Awards")

    print("time based categorie identification start")
    # additional step to match with real categories so during presenters  it would be easy to classify based on award type
    for year in resources.years:
        if year in [2013, 2015]:
            awards = resources.OFFICIAL_AWARDS_1315
        else:
            awards = resources.OFFICIAL_AWARDS_1819

        info_extract = InfoExtractor()
        for each_award in awards:
            clean_awards[each_award] = info_extract.clean_tweet(each_award)

        categorie_data[year]['real_categorie'] = categorie_data[year]['categorie'].apply(
            lambda x: fuzz_(x, clean_awards))
        categorie_data[year] = categorie_data[year].loc[categorie_data[year]['real_categorie'] != 'N/a', :]
        categorie_data[year].reset_index(drop=True, inplace=True)

        data_catg = categorie_data[year].groupby(['hour', 'minute', 'real_categorie']).count()[
            'clean_lower'].unstack().reset_index()
        data_catg = data_catg.dropna(how='all', axis=1)

        best_catg_time[year] = {}
        for each_ in list(data_catg.columns):
            if not each_ in ['hour', 'minute']:
                best_catg_time[year][each_] = []
                max_idx = data_catg[each_].idxmax()
                best_catg_time[year][each_].append(
                    (data_catg.iloc[max_idx - 2]['hour'], data_catg.iloc[max_idx - 2]['minute']))
                best_catg_time[year][each_].append(
                    (data_catg.iloc[max_idx - 1]['hour'], data_catg.iloc[max_idx - 1]['minute']))
                best_catg_time[year][each_].append((data_catg.iloc[max_idx]['hour'], data_catg.iloc[max_idx]['minute']))
                best_catg_time[year][each_].append(
                    (data_catg.iloc[max_idx + 1]['hour'], data_catg.iloc[max_idx + 1]['minute']))
                best_catg_time[year][each_].append(
                    (data_catg.iloc[max_idx + 2]['hour'], data_catg.iloc[max_idx + 2]['minute']))
    print("time based categorie identification end")

    # Load the wikidata from disk
    people = wikidata.call_wikidate('actors', 'actorLabel') + wikidata.call_wikidate('directors', 'directorLabel') + wikidata.call_wikidate('actresses', 'actorLabel')
    things = wikidata.call_wikidate('series', 'seriesLabel')
    people = [re.sub(r'[^\w\d\s]+', '', person_) for person_ in people]
    things = [re.sub(r'[^\w\d\s]+', '', thing_) for thing_ in things]

    # We search for the hosts
    print("Find Hosts")
    for year in resources.years:
        host_categorizer = TweetCategorizer([resources.HOST_WORDS], [], "host_tweet", resources.data[year], 0,
                                            resources.data[year].shape[0])
        host_tweets = host_categorizer.get_categorized_tweets()
        hosters = host_categorizer.find_percentage_of_entities(host_tweets, 0.2, people, [])
        results[year]["Hosts"] = hosters[resources.HOST_WORDS]
    print("Done Hosts\n")

    # Search for the winners
    print("Find Winners")
    for year in resources.years:
        all_winners[year] = []
        awards = resources.OFFICIAL_AWARDS_1315
        if year in [2018, 2019]:
            awards = resources.OFFICIAL_AWARDS_1819
        winner_categorizer = TweetCategorizer(awards, resources.STOPWORDS, "award", resources.data[year], 3,
                                              resources.data[year].shape[0])
        winner_tweets = winner_categorizer.get_categorized_tweets()
        winners = winner_categorizer.find_list_of_entities(winner_tweets, 1, people, things + wikidata.call_wikidate("films","filmLabel", str(year -2), str(year)))
        for key in winners:
            results[year][key] = {}
            if winners[key]:
                results[year][key]["Winner"] = winners[key][0]
            else:
                results[year][key]["Winner"] = ""
            all_winners[year].append(winners[key])
    print("Done Winners\n")

    print("Find Presenters")
    for year in resources.years:
        for key, value in best_catg_time[year].items():
            data_new = pd.DataFrame(columns=list(resources.data[year].columns))

            for each_value in value:
                data_temp = resources.data[year].loc[(resources.data[year].hour == int(each_value[0])), :]
                data_temp = data_temp.loc[(data_temp.minute == int(each_value[1])), :]
                data_new = pd.concat([data_new, data_temp])

            presenter_categorizer = TweetCategorizer([resources.PRESENTER_WORDS], [], "presenter_tweet", data_new, 0,
                                                     data_new.shape[0])
            presenter_tweets = presenter_categorizer.get_categorized_tweets()

            # presenters = find_names(presenter_tweets.clean_upper.tolist(),2,people,all_winners[year],results[year]["Hosts"])
            presenters = presenter_categorizer.find_list_of_entities(presenter_tweets, 3, people, [], people=True)
            presenters = [p for p in presenters[list(presenters.keys())[0]] if
                          (p not in all_winners[year]) and (p not in results[year]["Hosts"])]

            results[year][key]['Presenters'] = presenters[-3:]
            print(key, ' - ', presenters[-3:])

        if year in [2013, 2015]:
            awards = resources.OFFICIAL_AWARDS_1315
        else:
            awards = resources.OFFICIAL_AWARDS_1819

        for each_ in awards:
            if not each_ in best_catg_time[year].keys():
                results[year][each_]['Presenters'] = []
    print("End Presenters")

    print("Find Nominees")
    for year in resources.years:
        for key, value in best_catg_time[year].items():
            data_new = pd.DataFrame(columns=list(resources.data[year].columns))

            for each_value in value:
                data_temp = resources.data[year].loc[(resources.data[year].hour == int(each_value[0])), :]
                data_temp = data_temp.loc[(data_temp.minute == int(each_value[1])), :]
                data_new = pd.concat([data_new, data_temp])

            nominee_categorizer = TweetCategorizer([resources.NOMINEE_WORDS], [], "nominee_tweet", data_new, 0,
                                                   data_new.shape[0])
            nominee_tweets = nominee_categorizer.get_categorized_tweets()

            # presenters = find_names(presenter_tweets.clean_upper.tolist(),2,people,all_winners[year],results[year]["Hosts"])
            if ('actress' in key.split()):
                nominees = nominee_categorizer.find_list_of_entities(nominee_tweets, 6, wikidata.call_wikidate('actresses', 'actorLabel'), [], people=True)
            elif ('actor' in key.split()):
                nominees = nominee_categorizer.find_list_of_entities(nominee_tweets, 6, wikidata.call_wikidate('actors', 'actorLabel'), [], people=True)
            elif ('director' in key.split()):
                nominees = nominee_categorizer.find_list_of_entities(nominee_tweets, 6, wikidata.call_wikidate('directors', 'actorLabel'), [], people=True)
            else:
                nominees = nominee_categorizer.find_list_of_entities(nominee_tweets, 6, [], things + wikidata.call_wikidate("films","filmLabel", str(year -2), str(year)))

            nominees = [p for p in nominees[list(nominees.keys())[0]] if (p not in all_winners[year]) and (
                        p not in results[year]["Hosts"] and (p not in results[year][key]['Presenters']))]

            results[year][key]['Nominees'] = nominees[-6:]
            print(key, ' - ', nominees[-6:])

        if year in [2013, 2015]:
            awards = resources.OFFICIAL_AWARDS_1315
        else:
            awards = resources.OFFICIAL_AWARDS_1819

        for each_ in awards:
            if not each_ in best_catg_time[year].keys():
                results[year][each_]['Nominees'] = []
    print("End Nominees")

    # Search for best and worst dress
    print("Find Dresses")
    for year in resources.years:
        dress_categorizer = TweetCategorizer([resources.DRESS], [], "dress", resources.data[year], 0,
                                             resources.data[year].shape[0])
        dress_tweets = dress_categorizer.get_categorized_tweets()

        best_dress_categorizer = TweetCategorizer([resources.BEST_DRESS], [], "best_dress", dress_tweets, 0,
                                                  dress_tweets.shape[0])
        best_dress_tweets = best_dress_categorizer.get_categorized_tweets()
        probs_best = best_dress_categorizer.list_probabilities(best_dress_tweets, 3, people, [], people=True)
        best_dressed = list(probs_best.keys())
        representative_best_tweets = []
        for b in best_dressed:
            for index, row in best_dress_tweets.iterrows():
                if b in str(row["clean_upper"]):
                    representative_best_tweets.append(str(row["text"]))
                    break

        worst_dress_categorizer = TweetCategorizer([resources.WORST_DRESS], [], "worst_dress", dress_tweets, 0,
                                                   dress_tweets.shape[0])
        worst_dress_tweets = worst_dress_categorizer.get_categorized_tweets()
        probs_worst = worst_dress_categorizer.list_probabilities(worst_dress_tweets, 3, people, [], people=True)
        worst_dressed = list(probs_worst.keys())

        representative_worst_tweets = []
        for w in worst_dressed:
            for index, row in worst_dress_tweets.iterrows():
                if w in str(row["clean_upper"]):
                    representative_worst_tweets.append(str(row["text"]))
                    break

        results[year]["BestDressed"] = probs_best
        results[year]["WorstDressed"] = probs_worst
        results[year]["BestDressedTweets"] = representative_best_tweets
        results[year]["WorstDressedTweets"] = representative_worst_tweets
    print("Done Dresses\n")

    # Search for best and worst dress
    print("Find Jokes")
    # for year in resources.years:
    #     joke_categorizer = TweetCategorizer([resources.JOKES], [], "jokes", resources.data[year], 0, resources.data[year].shape[0])
    #     joke_tweets = joke_categorizer.get_categorized_tweets()
    #     funny_people = joke_categorizer.find_list_of_entities(joke_tweets, 5, people, [], people=True)[resources.JOKES]
    #     representative_joke_tweets = []
    #     for f in funny_people:
    #         for index, row in joke_tweets.iterrows():
    #             if f in str(row["clean_lower"]):
    #                 representative_joke_tweets.append(str(row["text"]))
    #                 break
    #     results[year]["JokeTweets"] = representative_joke_tweets
    #     results[year]["FunnyPeople"] = funny_people
    #
    #     moment_categorizer = TweetCategorizer([resources.MOMENTS], [], "moments", resources.data[year], 0, resources.data[year].shape[0])
    #     moment_tweets = moment_categorizer.get_categorized_tweets()
    #     link_finder = re.compile(r'http(s)?\:\/\/[\w\.\d]*\b')
    #     results[year]["Moments"] = {}
    #     for type in resources.MOMENT_TYPES:
    #         type_categorizer = TweetCategorizer([type], [], "jokes", moment_tweets, 0, moment_tweets.shape[0])
    #         type_tweets = type_categorizer.get_categorized_tweets()
    #         type_people = type_categorizer.find_list_of_entities(type_tweets, 1, people, [], people=True)[type]
    #         results[year]["Moments"][type] = {}
    #         results[year]["Moments"][type]["Person"] = type_people
    #         for index, row in type_tweets.iterrows():
    #             if type_people in str(row["clean_lower"]):
    #                 results[year]["Moments"][type]["Tweet"] = str(row["text"])
    #                 break
    #         http_categorizer = TweetCategorizer(["http"], [], "links", type_tweets, 0, type_tweets.shape[0],column="text")
    #         http_tweets = http_categorizer.get_categorized_tweets()
    #         print(str(http_tweets["text"][0]))
    #         link = link_finder.findall(str(http_tweets["text"][0]))
    #         results[year]["Moments"][type]["Link"] = link
    print("Done Jokes\n")

    markdown = ""
    for year in resources.years:

        markdown += "# " + str(year) + " Golden Globes\n"

        markdown += "## Hosts\n"
        for h in results[year]["Hosts"]:
            markdown += " - " + h + "\n"

        markdown += "## Best Dressed\n"
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

        markdown += "## Worst Dressed\n"
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
        markdown += "## Awards\n"
        for cat in awards:
            markdown += "### " + cat + "\n"
            # Presenters
            markdown += "#####Presenters:\n"
            for a in results[year][cat]['Presenters']:
                markdown += "- " + a + "\n"
            # Nominees
            markdown += "\n#####Nominees:\n"
            for a in results[year][cat]['Nominees']:
                markdown += " - " + a + "\n"
            # Winner
            markdown += "\n#####Winner- " + results[year][cat]['Winner'] + "\n"

    # Save the final results to disk
    with open('results.md', 'w') as file:
        file.write(markdown)

    with open("results.json", "w") as f:
        json.dump(results, f)
    return


if __name__ == '__main__':
    main()
    #pre_ceremony()
