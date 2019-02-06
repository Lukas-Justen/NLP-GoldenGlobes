import copy
import re


class TweetCategorizer:

    def __init__(self, group_indicators, stopwords, group_name, tweets, threshold, sample_size):
        group_indicators = sorted(group_indicators, key=len)
        self.tweets = tweets.sample(frac=1)[:sample_size]
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
        self.tweets = self.apply_indicators(self.group_indicators, group_name, self.tweets)

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
            print("Entity: ", self.winner[key], "Award: ", key)

