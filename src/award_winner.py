import copy
import re

import pandas as pd

data = pd.read_csv("../data/cleaned_gg2013.csv")

stopwords = ["an", "in", "a", "for", "by", "-", "or"]
awards = ['Best Performance by an Actress in a Television Series - Drama', 'Best Television Series - Comedy Or Musical',
          'Best Performance by an Actress in a Supporting Role in a Series', 'Best Motion Picture - Musical or Comedy',
          'Best Performance by an Actress in a Motion Picture - Comedy Or Musical', 'Best Television Series - Drama',
          'Best Performance by an Actress in a Television Series - Comedy Or Musical', 'Best Animated Feature Film',
          'Best Performance by an Actor in a Supporting Role in a Motion Picture', 'Best Director - Motion Picture',
          'Best Performance by an Actress in a Supporting Role in a Motion Picture', 'Best Motion Picture - Drama',
          'Best Performance by an Actress in a Motion Picture - Drama', 'Best Original Score - Motion Picture',
          'Best Performance by an Actor in a Motion Picture - Comedy or Musical', 'Best Foreign Language Film',
          'Best Performance by an Actor in a Television Series - Drama', 'Best Original Song - Motion Picture',
          'Best Performance by an Actor in a Supporting Role in a Series', 'Best Screenplay - Motion Picture',
          'Best Performance by an Actor in a Television Series - Comedy or Musical', 'cecil b demille award',
          'Best Performance by an Actress in a Mini-series or Motion Picture Made for Television',
          'Best Performance by an Actor in a Mini-Series or Motion Picture Made for Television',
          'Best Performance by an Actor in a Motion Picture - Drama',
          'Best Mini-Series or Motion Picture made for Television']

presenter_keywords = "present|presents|presenting|presented|presentation|presenter|presenters"
nominee_keywords = "nominee|nomination|nominated|nominees|nominations|nominate|vote|voting|voter|voted|candidate"
host_keywords = "host|hosting|hoster|hosts|anchor|entertainer|entertaining|moderator|moderating|moderated|entertained"


class TweetCategorizer:

    def __init__(self, group_indicators, stopwords, group_name, tweets, threshold, sample_size):
        group_indicators = sorted(group_indicators, key=len)
        tweets = tweets.sample(frac=1)[:sample_size]
        self.stripper = re.compile(r'\b(\w+)-(\w+)\b')
        self.bigram_finder = re.compile(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b')
        self.unigram_finder = re.compile(r'\b[A-Z][a-z]+\b')
        self.detecter = []
        self.replacor = []
        self.threshold = threshold
        self.winner = {}
        self.group_name = group_name
        self.original_groups = copy.deepcopy(group_indicators)
        self.group_indicators = self.strip_indicators(group_indicators, stopwords)
        self.tweets = self.apply_indicators(self.group_indicators, group_name, tweets)

    def strip_indicators(self, group_indicators, stopwords):
        for index in range(0, len(group_indicators)):
            text = str(group_indicators[index]).lower()
            text = " ".join("" if x in stopwords else x for x in text.split())
            matches = self.stripper.findall(text)
            for match in matches:
                text = text + " " + str(match[0]) + str(match[1])
            group_indicators[index] = "|".join(text.split())
            self.detecter.append(re.compile(str(group_indicators[index])))
            self.replacor.append(re.compile(str(group_indicators[index]), flags=re.IGNORECASE))
        return group_indicators

    def apply_indicators(self, group_indicators, group_name, tweets):
        tweets[group_name] = tweets["clean_text"].apply(lambda text: self.detect_group(text, group_indicators))
        return tweets

    def detect_group(self, text, group_indicators):
        counts_per_group = dict.fromkeys(range(0, len(group_indicators)), 0)
        text = str(text).lower()
        for index in range(0, len(group_indicators)):
            matches = self.detecter[index].findall(text)
            counts_per_group[index] = len(matches)
        max_value = max(counts_per_group.values())
        return max(counts_per_group, key=counts_per_group.get) if max_value > self.threshold else -1

    def get_categorized_tweets(self):
        categorized_tweets = self.tweets[self.tweets[self.group_name] > -1]
        categorized_tweets = categorized_tweets.sort_values(by=[self.group_name, "hour", "minute"])
        return categorized_tweets

    def count_entity_bigram(self, text, entity_count, category):
        text = self.replacor[category].sub(' ', text)
        matches = self.bigram_finder.findall(text)
        entity_count = self.aggregate_entity_count(matches, entity_count)
        return entity_count

    def count_entity_unigram(self, text, entity_count, category):
        text = self.replacor[category].sub(' ', text)
        matches = self.unigram_finder.findall(text)
        entity_count = self.aggregate_entity_count(matches, entity_count)
        return entity_count

    def aggregate_entity_count(self, matches, entity_count):
        for match in matches:
            entity_count[match] = 1 if match not in entity_count.keys() else entity_count[match] + 1
        return entity_count

    def find_frequent_entity(self, tweets):
        for i in range(0, len(self.group_indicators)):
            associated_tweets = tweets[tweets[self.group_name] == i]
            self.winner[self.original_groups[i]] = str(self.evaluate_entity_counts(i, associated_tweets)).lower()
        return self.winner

    def find_list_of_entities(self, tweets, number_entities):
        counts = {}
        for i in range(0, len(self.group_indicators)):
            _, people_count_bigram = self.count_entities(tweets, i)
            people_count_bigram = sorted(people_count_bigram, key=people_count_bigram.get, reverse=True)
            counts[self.original_groups[i]] = [people_count_bigram[i] for i in range(0, number_entities)]
        return counts

    def count_entities(self, tweets, group_index):
        people_count_bigram = {}
        people_count_unigram = {}
        for index, row in tweets.iterrows():
            people_count_bigram = self.count_entity_bigram(row['clean_text'], people_count_bigram, group_index)
            people_count_unigram = self.count_entity_unigram(row['clean_text'], people_count_unigram, group_index)
        # for key in sorted(people_count_unigram, key=people_count_unigram.get):
        #     print("Award: ", self.original_groups[group_index], "Word: ", key, "Count: ", people_count_unigram[key])
        # for key in sorted(people_count_bigram, key=people_count_bigram.get):
        #     print("Award: ", self.original_groups[group_index], "Word: ", key, "Count: ", people_count_bigram[key])
        return people_count_unigram, people_count_bigram

    def evaluate_entity_counts(self, group_index, tweets):
        people_count_unigram, people_count_bigram = self.count_entities(tweets, group_index)
        unigram_winner = max(people_count_unigram, key=people_count_unigram.get)
        bigram_winner = max(people_count_bigram, key=people_count_bigram.get)
        unigram_count = people_count_unigram[unigram_winner]
        bigram_count = people_count_bigram[bigram_winner]
        return unigram_winner if 3 * bigram_count < unigram_count else bigram_winner

    def print_frequent_entities(self):
        for key in sorted(self.winner):
            print("Winner: ", self.winner[key], "Award: ", key)

    def count_words(self, words, tweets, new_column):
        tweets[new_column] = tweets["clean_text"].apply(lambda text: self.count_words_in_text(text, words))
        return tweets

    def count_words_in_text(self, text, words):
        matches = re.findall(words, text)
        return len(matches)


# start = time.time()
# award_categorizer = TweetCategorizer(awards, stopwords, "award", data, 3, 1500000)
# award_tweets = award_categorizer.get_categorized_tweets()
# award_winner = award_categorizer.find_frequent_entity(award_tweets)
# award_categorizer.print_frequent_entities()
# end = time.time()
# print(end - start)

# nominee_categorizer = TweetCategorizer([nominee_keywords], stopwords, "category", data, 0, 1500000)
# nominee_tweets = nominee_categorizer.get_categorized_tweets()
# nominee_categorizer.find_frequent_entity(nominee_tweets)

# presenter_categorizer = TweetCategorizer([presenter_keywords], stopwords, "category", data, 0, 1500000)
# presenter_tweets = presenter_categorizer.get_categorized_tweets()
# presenter_categorizer.find_frequent_entity(presenter_tweets)

# host_categorizer = TweetCategorizer([host_keywords], stopwords, "category", data, 0, 1500000)
# host_tweets = host_categorizer.get_categorized_tweets()
# hosters = host_categorizer.find_list_of_entities(host_tweets, 2)
# print(hosters)

# TODO: Assign probability to each entity based on its appearance in the whole corpus
# TODO: Split long categories and short categories and adjust cutoff for match
# TODO: Unable to find winner message or output if dict is empty
# TODO: Setup Multiple matching so that the first 2-3 groups get assigned to a tweet

# print()
# def parse_json(file_name):
#     json_file = open(file_name, "r")
#     json_text = json_file.read()
#     return json.loads(json_text)
#
#
# def get_real_answer(answer_file):
#     parsed_json_2013 = parse_json(answer_file)
#     winners = {}
#     for award in sorted(parsed_json_2013["award_data"]):
#         winners[award] = parsed_json_2013["award_data"][award]["winner"]
#     return winners
#
#
# winners_actual = get_real_answer("../data/gg2013answers.json")
# for key in sorted(winners_actual):
#     print("Winner: ", winners_actual[key], "Award: ", key)
