import matplotlib.pyplot as plt
import seaborn as sns
from nltk import word_tokenize, Text, FreqDist, ngrams


class DataVisualizer:

    def __init__(self, data, column):
        self.data = data
        self.vocabulary = self.create_vocabulary(column)
        self.column = column

    def show_analysis(self):
        # General analysis for number of tweets, features and the text
        print('Total number of tweets: {}'.format(self.data.shape[0]))
        print('Features of dataframe: ', list(self.data.columns))
        print('Text of first tweet:   ', self.data[self.column][0])

        # Create a new column with the total word count for each tweet
        f, ax = plt.subplots(figsize=(20, 15))
        sns.countplot(self.data[self.column + "_wordcount"], ax=ax)
        plt.show()

    def create_vocabulary(self, column):
        # Setup the vocabulary for the ngrams
        tweet_list = list(self.data[column])
        tweet_text = ' '.join(map(str, tweet_list))
        tokens = word_tokenize(tweet_text)
        t = Text(tokens)
        t.vocab()
        return t

    def count_ngram(self, n):
        # Do ngrams and plot the top 30 ngrams
        bigram_freq = FreqDist(list(ngrams(self.vocabulary, n)))
        plt.subplots(figsize=(20, 15))
        bigram_freq.plot(50)
        plt.show()

    def count_ngram_with(self, n, word):
        # Build ngrams and only keep ngrams that start with the given word
        ngram_list = list(ngrams(self.vocabulary, n))
        special_list = []
        for gram in ngram_list:
            if gram[0] == word:
                special_list.append(gram)

        ngram_freq = FreqDist(special_list)
        for key in sorted(ngram_freq, key=ngram_freq.get):
            print(key, ngram_freq[key])
        plt.subplots(figsize=(20, 15))
        ngram_freq.plot(50)
        plt.show()
