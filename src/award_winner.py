import copy
import json
import re

import pandas as pd
from nltk import FreqDist, ngrams, word_tokenize, Text

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
        self.winner = {}
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

    def find_frequent_entities_from_list(self,tweets,entity_list):
        self.winner = {}
        for i in range(0, len(self.group_indicators)):
            associated_tweets = tweets[tweets[self.group_name] == i]
            self.winner[self.original_groups[i]] = str(self.evaluate_entity_count_from_list(i, associated_tweets, entity_list)).lower()
        return self.winner

    def evaluate_entity_count_from_list(self, group_index,tweets, allowed_entities):
        _, people_count_bigram = self.count_entities(tweets, group_index)
        people_count_bigram = {key: people_count_bigram[key] for key in people_count_bigram if key not in allowed_entities}
        people_count_bigram['NOTHING FOUND'] = 0
        bigram_winner = max(people_count_bigram, key=people_count_bigram.get)
        return bigram_winner

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
        people_count_unigram['NOTHING_FOUND'] = 0
        people_count_bigram['NOTHING FOUND'] = 0
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


def count_ngram(n, data, number_of_entities):
    vocabulary = create_vocabulary(data, "clean_text")
    bigram_freq = FreqDist(list(ngrams(vocabulary, n)))
    bigram_freq = sorted(bigram_freq, key=bigram_freq.get, reverse=True)
    ngram_entities = []
    for index in range(0, number_of_entities):
        ngram_entities.append(bigram_freq[index][0] + " " + bigram_freq[index][1])
    return ngram_entities


def create_vocabulary(data, column):
    # Setup the vocabulary for the ngrams
    tweet_list = list(data[column])
    tweet_text = ' '.join(map(str, tweet_list))
    tokens = word_tokenize(tweet_text)
    t = Text(tokens)
    t.vocab()
    return t

# award_categorizer = TweetCategorizer(awards, stopwords, "award", data, 3, 1500000)
# award_tweets = award_categorizer.get_categorized_tweets()
# award_tweets["absolute_time"] = award_tweets["hour"].apply(lambda hour: hour*60)
# award_tweets["absolute_time"] += award_tweets["minute"].apply(lambda minute: minute)
# average_time = award_tweets.groupby(['award']).mean()
# average_time = average_time.sort_values(by=["absolute_time","hour", "minute"])

# award_winner = award_categorizer.find_frequent_entity(award_tweets)
# award_categorizer.print_frequent_entities()

award_categorizer = TweetCategorizer(awards, stopwords, "award", data, 3, 1500000)
award_tweets = award_categorizer.get_categorized_tweets()
# bigrams = count_ngram(2, data, 400)
presenter_categorizer = TweetCategorizer([presenter_keywords], [], "category", data, 0, 1500000)
presenter_tweets = presenter_categorizer.get_categorized_tweets()
presenter_tweets = presenter_tweets.sort_values(by=["hour","minute"])
# presenters = presenter_categorizer.find_list_of_entities(presenter_tweets, 200)
# presenters = [p for p in presenters[presenter_keywords] if p in bigrams]
presenter_pattern = []
presenter_pattern.append(re.compile(r'([A-Z][a-zA-Z]* [A-Z][a-zA-Z]*) ([A-Z][a-zA-Z]* [A-Z][a-zA-Z]*) present'))
presenter_pattern.append(re.compile(r'[a-z]+ ([A-Z][a-zA-Z]* [A-Z][a-zA-Z]* [A-Z][a-zA-Z]*) presents'))
presenter_pattern.append(re.compile(r'[a-z]+ [a-z]+ ([A-Z][a-zA-Z]* [A-Z][a-zA-Z]*) presents'))
# presenter_pattern.append(re.compile(r'[pP][rR][eE][sS][eE][nN][tT]{[eE][dD]|[sS]|[iI][nN][gG]}{ by| BY| By| }[A-Z][a-zA-Z]* [A-Z][a-zA-Z]*'))
for index, row in presenter_tweets.iterrows():
    for p in presenter_pattern:
        matches = p.findall(row['clean_text'])
        for m in matches:
            print(m)
            # print(row['clean_text'])
# johan_hill = TweetCategorizer(['jonah'],[],"category",data,0,1500000)
# johan_hill_tweets = johan_hill.get_categorized_tweets()
print("END")
# award_presenters = award_categorizer.find_frequent_entities_from_list(award_tweets,presenters)
# award_categorizer.print_frequent_entities()

# nominee_categorizer = TweetCategorizer([nominee_keywords], [], "category", data, 0, 1500000)
# nominee_tweets = nominee_categorizer.get_categorized_tweets()
# nominees = nominee_categorizer.find_list_of_entities(nominee_tweets, 200)
# nominees = [n for n in nominees[nominee_keywords] if n in bigrams]
#
# print(bigrams)
# print(presenters)
# print(nominees)

# host_categorizer = TweetCategorizer([host_keywords], [], "category", data, 0, 1500000)
# host_tweets = host_categorizer.get_categorized_tweets()
# hosters = host_categorizer.find_list_of_entities(host_tweets, 2)
# print(hosters)

# TODO: Assign probability to each entity based on its appearance in the whole corpus
# TODO: Split long categories and short categories and adjust cutoff for match
# TODO: Unable to find winner message or output if dict is empty
# TODO: Setup Multiple matching so that the first 2-3 groups get assigned to a tweet

print()
def parse_json(file_name):
    json_file = open(file_name, "r")
    json_text = json_file.read()
    return json.loads(json_text)


def get_real_answer(answer_file):
    parsed_json_2013 = parse_json(answer_file)
    winners = {}
    for award in sorted(parsed_json_2013["award_data"]):
        winners[award] = parsed_json_2013["award_data"][award]["presenters"]
    return winners


winners_actual = get_real_answer("../data/gg2013answers.json")
for key in sorted(winners_actual):
    print("Winner: ", winners_actual[key], "Award: ", key)
