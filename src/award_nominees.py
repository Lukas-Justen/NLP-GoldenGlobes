import json
import re

import pandas as pd

data = pd.read_csv("../data/cleaned_gg2013.csv")

awards = ['Best Director - Motion Picture',
          'Best Screenplay - Motion Picture',
          'Best Foreign Language Film',
          'Best Animated Feature Film',
          'Best Original Score - Motion Picture',
          'Best Original Song - Motion Picture',
          'Best Motion Picture - Drama',
          'Best Motion Picture - Musical or Comedy',
          'Best Television Series - Drama',
          'Best Television Series - Comedy Or Musical',
          'Best Mini-Series or Motion Picture made for Television',
          'Best Performance by an Actress in a Motion Picture - Drama',
          'Best Performance by an Actress in a Motion Picture - Comedy Or Musical',
          'Best Performance by an Actress in a Supporting Role in a Series',
          'Best Performance by an Actress In a Supporting Role in a Motion Picture',
          'Best Performance by an Actress In a Television Series - Drama',
          'Best Performance by an Actress In a Television Series - Comedy Or Musical',
          'Best Performance by an Actress In a Mini-series or Motion Picture Made for Television',
          'Best Performance by an Actor in a Motion Picture - Drama',
          'Best Performance by an Actor in a Motion Picture - Comedy Or Musical',
          'Best Performance by an Actor in a Supporting Role in a Series',
          'Best Performance by an Actor In a Supporting Role in a Motion Picture',
          'Best Performance by an Actor In a Television Series - Drama',
          'Best Performance by an Actor In a Television Series - Comedy Or Musical',
          'Best Performance by an Actor in a Mini-Series or Motion Picture Made for Television',
          # 'cecil b. demille award'
          ]


def strip_awards(awards):
    stopwords = ["an", "in", "a", "for", "by", "-", "or", "best"]
    for index, award in enumerate(awards):
        awards[index] = awards[index].lower()
        for stopword in stopwords:
            awards[index] = awards[index].replace(" " + stopword + " ", " ")
        awards[index] = "|".join(awards[index].split())
    return awards


def check_for_words(text):
    counts_per_award = dict.fromkeys(range(0, len(awards)), 0)
    text = str(text).lower()
    for index, award in enumerate(awards):
        matches = re.findall(award, text)
        counts_per_award[index] = len(matches)
    max_value = max(counts_per_award.values())
    if max_value > 3:
        return max(counts_per_award, key=counts_per_award.get)
    return -1


def count_people(text, people_count, category):
    text = re.sub(awards[category], ' ', text, flags=re.IGNORECASE)
    matches = re.findall(r'[A-Z][a-z]* [A-Z][a-z]*', text)
    for match in matches:
        if match in people_count.keys():
            people_count[match] += 1
        else:
            people_count[match] = 1
    return people_count


def find_winner(data):
    winners = {}
    for i in range(0, len(awards)):
        associated_awards = data[data["award"] == i]
        people_count = {}
        for index, row in associated_awards.iterrows():
            people_count = count_people(row['clean_text'], people_count, i)
        winners[awards[i]] = max(people_count, key=people_count.get)
        for p in sorted(people_count, key=people_count.get, reverse=True):
            print("Award: ", awards[i], "Winner: ", p, "Count: ", people_count[str(p)])
    return winners


def parse_json(file_name):
    json_file = open(file_name, "r")
    json_text = json_file.read()
    return json.loads(json_text)


def get_real_answer(answer_file):
    parsed_json_2013 = parse_json(answer_file)
    winners = {}
    for award in sorted(parsed_json_2013["award_data"]):
        winners[award] = parsed_json_2013["award_data"][award]["winner"]
    return winners

awards = strip_awards(awards)
data["award"] = data["clean_text"].apply(lambda text: check_for_words(text))
award_tweets = data[data["award"] > -1]
award_tweets = award_tweets.sort_values(by=["award", "hour", "minute"])

winners_model = find_winner(award_tweets)
winners_actual = get_real_answer("../data/gg2013answers.json")


for key in sorted(winners_model):
    print("Winner: ", winners_model[key],"Award: ", key)
print()
for key in sorted(winners_actual):
    print("Winner: ", winners_actual[key],"Award: ", key)

# TODO: Assign importance to each award word based on appearance in other awards
# TODO: Draw a histogram that shows the number of award tweets per time in different colors
# TODO: Split long categories and short categories and adjust cutoff for match
