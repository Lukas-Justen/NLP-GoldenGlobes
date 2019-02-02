import re

import pandas as pd

data = pd.read_csv("../data/cleaned_gg2013.csv")

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
          'Best Performance by an Actor in a Television Series - Comedy or Musical', 'cecil b. demille award',
          'Best Performance by an Actress in a Mini-series or Motion Picture Made for Television',
          'Best Performance by an Actor in a Mini-Series or Motion Picture Made for Television',
          'Best Performance by an Actor in a Motion Picture - Drama',
          'Best Mini-Series or Motion Picture made for Television', ]

stopwords = ["an", "in", "a", "for", "by", "-", "or"]


class TweetCategorizer:

    def __init__(self, group_indicators, stopwords, group_name, tweets):
        self.group_indicators = self.strip_indicators(group_indicators, stopwords)
        self.tweets = self.apply_indicators(self.group_indicators, group_name, tweets)
        self.group_name = group_name
        self.winner = {}

    def strip_indicators(self, group_indicators, stopwords):
        group_indicators = sorted(group_indicators, key=len)
        for index in range(0, len(group_indicators)):
            text = str(group_indicators[index]).lower()
            text = " ".join("" if x in stopwords else x for x in text.split())
            group_indicators[index] = "|".join(text.split())
        return group_indicators

    def apply_indicators(self, group_indicators, group_name, tweets):
        tweets[group_name] = tweets["clean_text"].apply(lambda text: self.detect_group(text, group_indicators))
        return tweets

    def detect_group(self, text, group_indicators):
        counts_per_group = dict.fromkeys(range(0, len(group_indicators)), 0)
        text = str(text).lower()
        for index in range(0, len(group_indicators)):
            matches = re.findall(group_indicators[index], text)
            counts_per_group[index] = len(matches)
        max_value = max(counts_per_group.values())
        return max(counts_per_group, key=counts_per_group.get) if max_value > 3 else -1

    def get_categorized_tweets(self):
        categorized_tweets = self.tweets[self.tweets[self.group_name] > -1]
        categorized_tweets = categorized_tweets.sort_values(by=[self.group_name, "hour", "minute"])
        return categorized_tweets

    def count_entity_bigram(self, text, entity_count, category):
        text = re.sub(str(self.group_indicators[category]), ' ', text, flags=re.IGNORECASE)
        matches = re.findall(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', text)
        entity_count = self.aggregate_entity_count(matches, entity_count)
        return entity_count

    def count_entity_unigram(self, text, entity_count, category):
        text = re.sub(str(self.group_indicators[category]), ' ', text, flags=re.IGNORECASE)
        matches = re.findall(r'\b[A-Z][a-z]+\b', text)
        entity_count = self.aggregate_entity_count(matches, entity_count)
        return entity_count

    def aggregate_entity_count(self, matches, entity_count):
        for match in matches:
            entity_count[match] = 1 if match not in entity_count.keys() else entity_count[match] + 1
        return entity_count

    def find_frequent_entity(self, tweets):
        for i in range(0, len(self.group_indicators)):
            associated_tweets = tweets[tweets[self.group_name] == i]
            self.winner[self.group_indicators[i]] = self.evaluate_entity_counts(i, associated_tweets)
        return self.winner

    def evaluate_entity_counts(self, group_index, tweets):
        people_count_bigram = {}
        people_count_unigram = {}
        for index, row in tweets.iterrows():
            people_count_bigram = self.count_entity_bigram(row['clean_text'], people_count_bigram, group_index)
            people_count_unigram = self.count_entity_unigram(row['clean_text'], people_count_unigram, group_index)
        unigram_winner = max(people_count_unigram, key=people_count_unigram.get)
        bigram_winner = max(people_count_bigram, key=people_count_bigram.get)
        unigram_count = people_count_unigram[unigram_winner]
        bigram_count = people_count_bigram[bigram_winner]
        return unigram_winner if 3 * bigram_count < unigram_count else bigram_winner

    def print_frequent_entities(self, ):
        for key in sorted(award_winner):
            print("Winner: ", award_winner[key], "Award: ", key)


award_categorizer = TweetCategorizer(awards, stopwords, "award", data)
award_tweets = award_categorizer.get_categorized_tweets()
award_winner = award_categorizer.find_frequent_entity(award_tweets)
award_categorizer.print_frequent_entities()

# TODO: Assign probability to each entity based on its appearance in the whole corpus
# TODO: Draw a histogram that shows the number of award tweets per time in different colors
# TODO: Split long categories and short categories and adjust cutoff for match
# TODO: Unable to find winner message or output if dict is empty
