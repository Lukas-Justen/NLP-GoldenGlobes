import glob
import os
import re
import time
import zipfile

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from nltk import TweetTokenizer, word_tokenize, Text, FreqDist, ngrams
from nltk.corpus import stopwords

regex_sub_s = re.compile(r"\'s")
regex_sub_rt = re.compile(r"RT ")
regex_sub_ve = re.compile(r"\'ve")
regex_sub_cant = re.compile(r"can\'t")
regex_sub_nt = re.compile(r"n\'t")
regex_sub_iam = re.compile(r"i\'m")
regex_sub_are = re.compile(r"\'re")
regex_sub_would = re.compile(r"\'d")
regex_sub_will = re.compile(r"\'ll")
regex_sub_am = re.compile(r"\'m")

regex_sub_link = re.compile(r'http(s)?\:\/\/[\w\.\d\/]*\b')
regex_sub_hashtags = re.compile(r'#\w*')
regex_sub_people = re.compile(r'@[^ ]*\b')
regex_sub_numbers = re.compile(r'\b\d+\b')
regex_sub_spaces = re.compile(r'\s+')
regex_sub_single_characters = re.compile(r'[\b^][A-Za-z][\b$]')


def load_data(path, year):
    # Load the specified zip file and put the data into a dataframe
    allFiles = glob.glob(path + "*.zip")
    for file in allFiles:
        zip_file = zipfile.ZipFile(file)
        file_info = zip_file.infolist()
        if str(year) in os.path.basename(file_info[0].filename):
            return pd.read_json(zip_file.open(file_info[0].filename))


def show_analysis(data, text_column, new_count_column):
    # General analysis for number of tweets, features and the text
    print('Total number of tweets: {}'.format(data.shape[0]))
    print('Features of dataframe: ', list(data.columns))
    print('Text of first tweet:   ', data[text_column][0])

    # Create a new column with the total word count for each tweet
    data = count_words_per_tweet(data, text_column, new_count_column)
    f, ax = plt.subplots(figsize=(20, 15))
    sns.countplot(data[new_count_column], ax=ax)
    plt.show()


def get_stopwords():
    # Specify the stopwords but keep versions of win and lose
    set_of_stopwords = stopwords.words('english') + ['goldenglobes', 'golden', 'Golden', 'Globes', 'Globe', 'globe',
                                                     'Yes', 'yes', 'No', 'no', 'He', 'he', 'She', 'she', 'OKAY',
                                                     'Okay', 'globes', '.com', 'rt', 'RT', 'ok', 'OK', 'And',
                                                     '.ly', '.net', '.org', 'aahh', 'aarrgghh', 'abt', 'ftl', 'ftw',
                                                     'fu', 'fuck', 'fucks', 'gtfo', 'gtg', 'haa', 'hah', 'hahah',
                                                     'haha', 'hahaha', 'hahahaha', 'hehe', 'heh', 'hehehe', 'hi',
                                                     'hihi', 'hihihi', 'http', 'https', 'huge', 'huh', 'huhu', 'huhuhu',
                                                     'idk', 'iirc', 'im', 'imho', 'imo', 'ini', 'irl', 'ish', 'isn',
                                                     'isnt', 'j/k', 'jk', 'jus', 'just', 'justwit', 'juz', 'kinda',
                                                     'kthx', 'kthxbai', 'kyou', 'laa', 'laaa', 'lah', 'lanuch', 'leavg',
                                                     'leh', 'lol', 'lols', 'ltd', 'mph', 'mrt', 'msg', 'msgs',
                                                     'muahahahahaha', 'nb', 'neways', 'ni', 'nice', 'pls', 'plz',
                                                     'plzz', 'psd', 'pte', 'pwm', 'pwned', 'qfmft', 'qft', 'tis', 'tm',
                                                     'tmr', 'tyty', 'tyvm', 'um', 'umm', 'viv', 'vn', 'vote', 'voted',
                                                     'w00t', 'wa', 'wadever', 'wah', 'wasn', 'wasnt', 'wassup', 'wat',
                                                     'watcha', 'wateva', 'watever', 'watnot', 'wats', 'wayy', 'wb',
                                                     'weren', 'werent', 'whaha', 'wham', 'whammy', 'whaow', 'whatcha',
                                                     'whatev', 'whateva', 'whatevar', 'whatever', 'whatnot', 'whats',
                                                     'whatsoever', 'whatz', 'whee', 'whenz', 'whey', 'whore', 'whores',
                                                     'whoring', 'win', 'wo', 'woah', 'woh', 'wooohooo', 'woot', 'wow',
                                                     'wrt', 'wtb', 'wtf', 'wth', 'wts', 'wtt', 'www', 'xs', 'ya',
                                                     'yaah', 'yah', 'yahh', 'yahoocurrency', 'yall', 'yar', 'yay',
                                                     'yea', 'yeah', 'yeahh', 'yeh', 'yhoo', 'ymmv', 'young', 'youre',
                                                     'yr', 'yum', 'yummy', 'yumyum', 'yw', 'zomg', 'zz', 'zzz', 'loz',
                                                     'lor', 'loh', 'tsk', 'meh', 'lmao', 'wanna', 'doesn', 'liao',
                                                     'didn', 'didnt', 'omg', 'ohh', 'ohgod', 'hoh', 'hoo', 'bye',
                                                     'byee', 'byeee', 'byeeee', 'lmaolmao', 'yeah.1', 'yeahh.1',
                                                     'yeahhh', 'yeahhhh', 'yeahhhhh', 'yup', 'yupp', 'hahahahahahaha',
                                                     'hahahahahah', 'hahhaha', 'wooohoooo', 'wahaha', 'haah', '2moro',
                                                     'veh', 'noo', 'nooo', 'noooo', 'hahas', 'ooooo', 'ahahaha',
                                                     'ahahahahah', 'tomolow', '.com.1', '.ly.1', '.net.1', '.org.1',
                                                     'aahh.1', 'aarrgghh.1', 'abt.1', 'accent', 'accented', 'accents',
                                                     'acne', 'ads', 'afaik', 'aft', 'ago', 'ahead', 'ain', 'aint',
                                                     'aircon', 'alot', 'am', 'annoy', 'annoyed', 'annoys', 'anycase',
                                                     'anymore', 'app', 'apparently', 'apps', 'argh', 'ass', 'asses',
                                                     'awesome', 'babeh', 'bad', 'bai', 'based', 'bcos', 'bcoz', 'bday',
                                                     'bit', 'biz', 'blah', 'bleh', 'bless', 'blessed', 'blk',
                                                     'blogcatalog', 'bro', 'bros', 'btw', 'byee.1', 'com', 'congrats',
                                                     'contd', 'conv', 'cos', 'cost', 'costs', 'couldn', 'couldnt',
                                                     'cove', 'coves', 'coz', 'crap', 'cum', 'curnews', 'curr', 'cuz',
                                                     'dat', 'de', 'didn.1', 'didnt.1', 'diff', 'dis', 'doc', 'doesn.1',
                                                     'doesnt', 'don', 'dont', 'dr', 'dreamt', 'drs', 'due', 'dun',
                                                     'dunno', 'duper', 'eh', 'ehh', 'emo', 'emos', 'eng', 'esp',
                                                     'fadein', 'ffs', 'fml', 'frm', 'ftl.1', 'ftw.1', 'fu.1', 'fuck.1',
                                                     'fucks.1', 'fwah', 'g2g', 'gajshost', 'gd', 'geez', 'gg', 'gigs',
                                                     'gtfo.1', 'gtg.1', 'haa.1', 'haha.1', 'hahaha.1', 'hasn', 'hasnt',
                                                     'hav', 'haven', 'havent', 'hee', 'heh.1', 'hehe.1', 'hehehe.1',
                                                     'hello', 'hey', 'hi.1', 'hmm', 'ho', 'hohoho', 'http.1', 'https.1',
                                                     'huh.1', 'huhu.1', 'huhuhu.1', 'idk.1', 'iirc.1', 'im.1', 'imho.1',
                                                     'imo.1', 'info', 'ini.1', 'irl.1', 'ish.1', 'isn.1', 'isnt.1',
                                                     'issued', 'j/k.1', 'jk.1', 'jus.1', 'just.1', 'justwit.1', 'juz.1',
                                                     'kinda.1', 'kthx.1', 'kthxbai.1', 'kyou.1', 'laa.1', 'laaa.1',
                                                     'lah.1', 'lanuch.1', 'lawl', 'leavg.1', 'leh.1', 'lfg', 'lfm',
                                                     'll', 'lmao.1', 'lmfao', 'lnks', 'lol.1', 'lols.1', 'lotsa',
                                                     'lotta', 'ltd.1', 'luv', 'ly', 'macdailynews', 'meh.1', 'mph.1',
                                                     'msg.1', 'msgs.1', 'muahahahahaha.1', 'nb.1', 'neato', 'ni.1',
                                                     'nite', 'nom', 'noscript', 'nvr', 'nw', 'ohayo', 'omfg', 'omfgwtf',
                                                     'omg.1', 'omgwtfbbq', 'omw', 'org', 'pf', 'pic', 'pls.1', 'plz.1',
                                                     'plzz.1', 'pm', 'pmsing', 'ppl', 'pre', 'pro', 'psd.1', 'pte.1',
                                                     'pwm.1', 'pwned.1', 'qfmft.1', 'qft.1', 'rawr', 'rawrr', 'rofl',
                                                     'roflmao', 'rss', 'rt', 'sec', 'secs', 'seem', 'seemed', 'seems',
                                                     'sgreinfo', 'shd', 'shit', 'shits', 'shitz', 'shld', 'shouldn',
                                                     'shouldnt', 'shudder', 'sq', 'sqft', 'sqm', 'srsly', 'stfu',
                                                     'stks', 'su', 'suck', 'sucked', 'sucks', 'suckz', 'sux', 'swf',
                                                     'tart', 'tat', 'tgif', 'thanky', 'thk', 'thks', 'tht', 'tired',
                                                     'tis.1', 'tm.1', 'tmr.1', 'tsk.1', 'ttyl', 'ty', 'tym', 'tyme',
                                                     'typed', 'tyty.1', 'tyvm.1', 'um.1', 'umm.1', 'va', 'valid',
                                                     'valids', 'var', 'vc', 've', 'viv.1', 'vn.1', 'w00t.1', 'wa.1',
                                                     'wadever.1', 'wah.1', 'wasn.1', 'wasnt.1', 'wassup.1', 'wat.1',
                                                     'watcha.1', 'wateva.1', 'watnot.1', 'wats.1', 'wayy.1', 'wb.1',
                                                     'web', 'website', 'websites', 'weren.1', 'werent.1', 'whaha.1',
                                                     'wham.1', 'whammy.1', 'whaow.1', 'whatcha.1', 'whatev.1',
                                                     'whateva.1', 'whatevar.1', 'whatever.1', 'whatnot.1', 'whats.1',
                                                     'whatsoever.1', "what's", 'whatz.1', 'whee.1', 'whenz.1', 'whey.1',
                                                     'whore.1', 'whores.1', 'whoring.1', 'wo.1', 'woah.1', 'woh.1',
                                                     'wooohooo.1', 'woot.1', 'wow.1', 'wrt.1', 'wtb.1', 'wtf.1',
                                                     'wth.1', 'wts.1', 'wtt.1', 'www.1', 'xs.1', 'ya.1', 'yaah.1',
                                                     'yah.1', 'yahh.1', 'yahoocurrency.1', 'yall.1', 'yar.1', 'yay.1',
                                                     'yea.1', 'yeah.2', 'yeahh.2', 'year', 'yearly', 'years', 'yeh.1',
                                                     'yhoo.1', 'ymmv.1', 'young.1', 'youre.1', 'yr.1', 'yum.1',
                                                     'yummy.1', 'yumyum.1', 'yw.1', 'zomg.1', 'zz.1', 'zzz.1',
                                                     'fucking', 'mrs', 'mr', 'eh.1', 'ehh.1', 'ehhh', 'lot', 'lots',
                                                     'http.2', 'html', 'com.1', 'ly.1', 'net', 'org.1',
                                                     'hahahahahahahahaha', 'hahahahaha', 'hahahahah', 'zzzzz',
                                                     '#teamfollowback', '#teamfollow', '#follow', '#autofollow',
                                                     '#followgain', '#followbackk', '#teamautofollow', '#followme',
                                                     '#ifollow', '#followngain', '#followback', '#followfriday',
                                                     '#ifollowback', '#200aday', '#500aday', '#1000aday', 'hahahahha',
                                                     'lolololol', 'lololol', 'lolol', 'lol.2', 'dude', 'hmmm', 'humm',
                                                     'tumblr', 'kkkk', 'fk', 'yayyyyyy', 'fffffffuuuuuuuuuuuu', 'zzzz',
                                                     'zzzzz.1', 'noooooooooo', 'noo.1', 'nooo.1', 'noooo.1',
                                                     'hahahhaha', 'woohoo', 'lalalalalalala', 'lala', 'lalala',
                                                     'lalalala', 'whahahaahahahahahah', 'hahahahahahahahahahaha',
                                                     'watching', 'watch']
    lst = ['won', 'wins', 'win', 'winning', 'lost', 'loss', 'losing']
    for word in lst:
        set_of_stopwords[:] = (value for value in set_of_stopwords if value != word)
    return set_of_stopwords


def clean_tweet(tweet, stopwords):
    # Remove all links hashtags and other things that are not words

    tweet = regex_sub_s.sub(" ", tweet)
    tweet = regex_sub_rt.sub("", tweet)
    tweet = regex_sub_ve.sub(" have ", tweet)
    tweet = regex_sub_cant.sub("cannot ", tweet)
    tweet = regex_sub_nt.sub(" not ", tweet)
    tweet = regex_sub_iam.sub("i am ", tweet)
    tweet = regex_sub_are.sub(" are ", tweet)
    tweet = regex_sub_would.sub(" would ", tweet)
    tweet = regex_sub_will.sub(" will ", tweet)
    tweet = regex_sub_am.sub(" am ", tweet)

    tweet = regex_sub_link.sub(' ', tweet)  # remove links
    tweet = regex_sub_hashtags.sub('', tweet)  # remove hastag
    tweet = regex_sub_people.sub(' ', tweet)  # remove at tags
    tweet = regex_sub_numbers.sub(' ', tweet)  # remove numbers
    tweet = regex_sub_spaces.sub(' ', tweet)  # remove whitespaces
    tweet = tweet.lstrip(' ')  # moves single space left
    tweet = ''.join(c for c in tweet if (c <= u'\u007a' and c >= u'\u0061') or (
            c <= u'\u005a' and c >= u'\u0041') or c == u'\u0020')  # remove emojis
    tweet = regex_sub_single_characters.sub("", tweet)

    tknzr = TweetTokenizer(preserve_case=True, reduce_len=True, strip_handles=True)  # reduce length of string
    tw_list = tknzr.tokenize(tweet)
    list_no_stopwords = [i for i in tw_list if i not in stopwords]

    tweet = ' '.join(list_no_stopwords)
    return tweet


def clean_dataframe_column(data, to_clean, new_col, stopwords):
    # Clean the specified column and return the whole dataframe
    data[new_col] = data[to_clean].apply(lambda x: clean_tweet(x, stopwords))
    return data


def count_words_per_tweet(data, to_count, col_name):
    # Count the words in the spciefied column and safe it to a new column
    data[col_name] = data[to_count].apply(lambda x: len(x.split()))
    return data


def drop_column(data, column):
    # Drops the specified column of the given dataframe
    data = data.drop([column], axis=1)
    return data


def convert_time(data, to_convert):
    # Convert the specified columns timestamp to hour and time
    data["hour"] = data[to_convert].apply(lambda x: x.hour)
    data["minute"] = data[to_convert].apply(lambda x: x.minute)
    return data


def create_vocabulary(data, column):
    # Setup the vocabulary for the ngrams
    tweet_list = list(data[column])
    tweet_text = ' '.join(map(str, tweet_list))
    tokens = word_tokenize(tweet_text)
    t = Text(tokens)
    t.vocab()
    return t


def count_ngram(n, vocabulary):
    # Do ngrams and plot the top 30 ngrams
    bigram_freq = FreqDist(list(ngrams(vocabulary, n)))
    plt.subplots(figsize=(20, 15))
    bigram_freq.plot(50)
    plt.show()


def count_ngram_with(n, word, vocabulary):
    # Build ngrams and only keep ngrams that start with the given word
    ngram_list = list(ngrams(vocabulary, n))
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


def save_dataframe(data, file):
    # Save the dataframe on disk
    data.to_csv(file, index=False)


def read_dataframe(file):
    # Read a dataframe from disk
    return pd.read_csv(file)


# print("Load the Data:")
# data = load_data('../data/', 2013)
# print("Done\n")
#
# print("Show pre Analysis:")
# show_analysis(data, "text", "total_words_before")
# print("Done\n")
# print("Clean the Dataframe:")
# start = time.time()
# custom_stopwords = get_stopwords()
# data = clean_dataframe_column(data, 'text', 'clean_text', custom_stopwords)
# end = time.time()
# print(end - start)
# print("Done\n")
#
# print("Show post Analysis:")
# show_analysis(data, "clean_text", "total_words_after")
# print("Done\n")
#
# print("Convert Time and Drop Columns:")
# data = data.loc[data['total_words_after'] > 1, :]
# data = convert_time(data, "timestamp_ms")
# data = drop_column(data, "user")
# data = drop_column(data, "id")
# data = drop_column(data, "timestamp_ms")
# print("Done\n")
#
# save_dataframe(data, "../data/cleaned_gg2013.csv")

data = read_dataframe("../data/cleaned_gg2013.csv")

print("Count N-Grams:")
vocabulary = create_vocabulary(data, "clean_text")
for i in range(5, 7):
    count_ngram_with(i,'best', vocabulary)
print("Done\n")
