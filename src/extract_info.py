#!/usr/bin/env python
# coding: utf-8

# In[473]:


import glob
import os
import zipfile

import pandas as pd

import warnings
warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt
import seaborn as sns


# In[474]:


def dataFrames(path,year):
        allFiles = glob.glob(path + "*.zip")
        for file in allFiles:
            zip_file = zipfile.ZipFile(file)
            file_info = zip_file.infolist()
            if str(year) in os.path.basename(file_info[0].filename):
               return pd.read_json(zip_file.open(file_info[0].filename))


# In[477]:


data = dataFrames('../data/',2013)


# In[478]:


# analysis of data set
print ('Total number of tweets - {}'.format(data.shape[0]))
print ('Features in the dataframe - ', list(data.columns))


# In[479]:


# Columns id, timestamp, user is not required
data = data[['text']]


# In[480]:


# number of words in each tweet to analyse the variance in text
data['total_words'] = data.text.apply(lambda x: len(x.split()))


# In[481]:


f, ax = plt.subplots(figsize=(20,15))
sns.countplot(data.total_words)


# In[483]:


import re
import nltk
from string import punctuation
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.tokenize import TweetTokenizer

set_ = stopwords.words('english') + ['goldenglobes','golden','globes','.com','.ly', '.net', '.org', 'aahh', 'aarrgghh',
'abt', 'ftl', 'ftw', 'fu', 'fuck', 'fucks', 'gtfo', 'gtg', 'haa', 'hah', 'hahah', 'haha', 'hahaha', 'hahahaha', 'hehe', 
'heh', 'hehehe', 'hi', 'hihi', 'hihihi', 'http', 'https', 'huge', 'huh', 'huhu', 'huhuhu', 'idk', 'iirc', 'im', 
'imho', 'imo', 'ini', 'irl', 'ish', 'isn', 'isnt', 'j/k', 'jk', 'jus', 'just', 'justwit', 'juz', 'kinda', 'kthx', 
'kthxbai', 'kyou', 'laa', 'laaa', 'lah', 'lanuch', 'leavg', 'leh', 'lol', 'lols', 'ltd', 'mph', 'mrt', 'msg', 'msgs',
'muahahahahaha', 'nb', 'neways', 'ni', 'nice', 'pls', 'plz', 'plzz', 'psd', 'pte', 'pwm', 'pwned', 'qfmft', 'qft', 
'tis', 'tm', 'tmr', 'tyty', 'tyvm', 'um', 'umm', 'viv', 'vn', 'vote', 'voted', 'w00t', 'wa', 'wadever', 'wah', 'wasn', 
'wasnt', 'wassup', 'wat', 'watcha', 'wateva', 'watever', 'watnot', 'wats', 'wayy', 'wb', 'weren', 'werent', 'whaha', 
'wham', 'whammy', 'whaow', 'whatcha', 'whatev', 'whateva', 'whatevar', 'whatever', 'whatnot', 'whats', 'whatsoever', 
'whatz', 'whee', 'whenz', 'whey', 'whore', 'whores', 'whoring', 'win', 'wo', 'woah', 'woh', 'wooohooo', 'woot', 'wow', 
'wrt', 'wtb', 'wtf', 'wth', 'wts', 'wtt', 'www', 'xs', 'ya', 'yaah', 'yah', 'yahh', 'yahoocurrency', 'yall', 'yar', 
'yay', 'yea', 'yeah', 'yeahh', 'yeh', 'yhoo', 'ymmv', 'young', 'youre', 'yr', 'yum', 'yummy', 'yumyum', 'yw', 'zomg', 
'zz', 'zzz', 'loz', 'lor', 'loh', 'tsk', 'meh', 'lmao', 'wanna', 'doesn', 'liao', 'didn', 'didnt', 'omg', 'ohh', 
'ohgod', 'hoh', 'hoo', 'bye', 'byee', 'byeee', 'byeeee', 'lmaolmao', 'yeah.1', 'yeahh.1', 'yeahhh', 'yeahhhh', 
'yeahhhhh', 'yup', 'yupp', 'hahahahahahaha', 'hahahahahah', 'hahhaha', 'wooohoooo', 'wahaha', 'haah', '2moro',
'veh', 'noo', 'nooo', 'noooo', 'hahas', 'ooooo', 'ahahaha', 'ahahahahah', 'tomolow', '.com.1', '.ly.1', '.net.1', 
'.org.1', 'aahh.1', 'aarrgghh.1', 'abt.1', 'accent', 'accented', 'accents', 'acne', 'ads', 'afaik', 'aft', 'ago', 
'ahead', 'ain', 'aint', 'aircon', 'alot', 'am', 'annoy', 'annoyed', 'annoys', 'anycase', 'anymore', 'app', 
'apparently', 'apps', 'argh', 'ass', 'asses', 'awesome', 'babeh', 'bad', 'bai', 'based', 'bcos', 'bcoz', 'bday', 
'bit', 'biz', 'blah', 'bleh', 'bless', 'blessed', 'blk', 'blogcatalog', 'bro', 'bros', 'btw', 'byee.1', 'com', 
'congrats', 'contd', 'conv', 'cos', 'cost', 'costs', 'couldn', 'couldnt', 'cove', 'coves', 'coz', 'crap', 'cum',
'curnews', 'curr', 'cuz', 'dat', 'de', 'didn.1', 'didnt.1', 'diff', 'dis', 'doc', 'doesn.1', 'doesnt', 'don', 'dont',
'dr', 'dreamt', 'drs', 'due', 'dun', 'dunno', 'duper', 'eh', 'ehh', 'emo', 'emos', 'eng', 'esp', 'fadein', 'ffs', 
'fml', 'frm', 'ftl.1', 'ftw.1', 'fu.1', 'fuck.1', 'fucks.1', 'fwah', 'g2g', 'gajshost', 'gd', 'geez', 'gg', 'gigs', 
'gtfo.1', 'gtg.1', 'haa.1', 'haha.1', 'hahaha.1', 'hasn', 'hasnt', 'hav', 'haven', 'havent', 'hee', 'heh.1', 'hehe.1',
'hehehe.1', 'hello', 'hey', 'hi.1', 'hmm', 'ho', 'hohoho', 'http.1', 'https.1', 'huh.1', 'huhu.1', 'huhuhu.1', 
'idk.1', 'iirc.1', 'im.1', 'imho.1', 'imo.1', 'info', 'ini.1', 'irl.1', 'ish.1', 'isn.1', 'isnt.1', 'issued', 
'j/k.1', 'jk.1', 'jus.1', 'just.1', 'justwit.1', 'juz.1', 'kinda.1', 'kthx.1', 'kthxbai.1', 'kyou.1', 'laa.1', 
'laaa.1', 'lah.1', 'lanuch.1', 'lawl', 'leavg.1', 'leh.1', 'lfg', 'lfm', 'll', 'lmao.1', 'lmfao', 'lnks', 'lol.1', 
'lols.1', 'lotsa', 'lotta', 'ltd.1', 'luv', 'ly', 'macdailynews', 'meh.1', 'mph.1', 'msg.1', 'msgs.1', 'muahahahahaha.1', 
'nb.1', 'neato', 'ni.1', 'nite', 'nom', 'noscript', 'nvr', 'nw', 'ohayo', 'omfg', 'omfgwtf', 'omg.1', 'omgwtfbbq', 
'omw', 'org', 'pf', 'pic', 'pls.1', 'plz.1', 'plzz.1', 'pm', 'pmsing', 'ppl', 'pre', 'pro', 'psd.1', 'pte.1', 
'pwm.1', 'pwned.1', 'qfmft.1', 'qft.1', 'rawr', 'rawrr', 'rofl', 'roflmao', 'rss', 'rt', 'sec', 'secs', 'seem', 
'seemed', 'seems', 'sgreinfo', 'shd', 'shit', 'shits', 'shitz', 'shld', 'shouldn', 'shouldnt', 'shudder', 'sq', 
'sqft', 'sqm', 'srsly', 'stfu', 'stks', 'su', 'suck', 'sucked', 'sucks', 'suckz', 'sux', 'swf', 'tart', 'tat', 'tgif',
'thanky', 'thk', 'thks', 'tht', 'tired', 'tis.1', 'tm.1', 'tmr.1', 'tsk.1', 'ttyl', 'ty', 'tym', 'tyme', 'typed', 'tyty.1', 
'tyvm.1', 'um.1', 'umm.1', 'va', 'valid', 'valids', 'var', 'vc', 've', 'viv.1', 'vn.1', 'w00t.1', 'wa.1', 'wadever.1',
'wah.1', 'wasn.1', 'wasnt.1', 'wassup.1', 'wat.1', 'watcha.1', 'wateva.1', 'watnot.1', 'wats.1', 'wayy.1', 'wb.1', 'web', 
'website', 'websites', 'weren.1', 'werent.1', 'whaha.1', 'wham.1', 'whammy.1', 'whaow.1', 'whatcha.1', 'whatev.1', 'whateva.1', 
'whatevar.1', 'whatever.1', 'whatnot.1', 'whats.1', 'whatsoever.1',"what's",'whatz.1', 'whee.1', 'whenz.1', 'whey.1', 'whore.1', 
'whores.1', 'whoring.1', 'wo.1', 'woah.1', 'woh.1', 'wooohooo.1', 'woot.1', 'wow.1', 'wrt.1', 'wtb.1', 'wtf.1', 'wth.1',
'wts.1', 'wtt.1', 'www.1', 'xs.1', 'ya.1', 'yaah.1', 'yah.1', 'yahh.1', 'yahoocurrency.1', 'yall.1', 'yar.1', 'yay.1',
'yea.1', 'yeah.2', 'yeahh.2', 'year', 'yearly', 'years', 'yeh.1', 'yhoo.1', 'ymmv.1', 'young.1', 'youre.1', 'yr.1', 
'yum.1', 'yummy.1', 'yumyum.1', 'yw.1', 'zomg.1', 'zz.1', 'zzz.1', 'fucking', 'mrs', 'mr', 'eh.1', 'ehh.1', 'ehhh', 
'lot', 'lots', 'http.2', 'html', 'com.1', 'ly.1', 'net', 'org.1', 'hahahahahahahahaha', 'hahahahaha', 'hahahahah', 
'zzzzz', '#teamfollowback', '#teamfollow', '#follow', '#autofollow', '#followgain', '#followbackk', '#teamautofollow',
'#followme', '#ifollow', '#followngain', '#followback', '#followfriday', '#ifollowback', '#200aday', '#500aday', 
'#1000aday', 'hahahahha', 'lolololol', 'lololol', 'lolol', 'lol.2', 'dude', 'hmmm', 'humm', 'tumblr', 'kkkk', 'fk',
'yayyyyyy', 'fffffffuuuuuuuuuuuu', 'zzzz', 'zzzzz.1', 'noooooooooo', 'noo.1', 'nooo.1', 'noooo.1', 'hahahhaha', 
'woohoo', 'lalalalalalala', 'lala', 'lalala', 'lalalala', 'whahahaahahahahahah','hahahahahahahahahahaha','watching','watch']


try:
    lst = ['won','wins','win','winning','lost','loss','losing' ]
    for word in lst:
        set_[:] = (value for value in set_ if value != word)
except:
    pass

def general_clean(tweet):
    tweet = tweet.lower()
     
    tweet = re.sub(r'https?:\/\/.*\/\w*', '', tweet) # remove links
    tweet = re.sub(r'#\w*', '', tweet) # remove hastag
    tweet = re.sub(r'[' + punctuation.replace('@', '') + ']+', ' ', tweet) # remove punctuations
	tweet = re.sub(r'\b\d+\b',' ',tweet)
    tweet = re.sub(r'\s+', ' ', tweet) # remove whitespaces
    tweet = tweet.lstrip(' ') # moves single space left
    tweet = ''.join(c for c in tweet if c <= '\uFFFF') # remove emojis
    
    tknzr = TweetTokenizer(preserve_case=False, reduce_len=True, strip_handles=True) # reduce length from waaaaaayyyy to waaayyy.
    tw_list = tknzr.tokenize(tweet)
    list_no_stopwords = [i for i in tw_list if i not in set_]
    
    tweet =' '.join(list_no_stopwords)
    return tweet


# In[484]:


data['clean_text'] = data.text.apply(lambda x:general_clean(x))


# In[485]:


data


# In[465]:


data = data[['clean_text']]
data['total_words'] = data.clean_text.apply(lambda x: len(x.split()))


# In[466]:


f, ax = plt.subplots(figsize=(20,15))
sns.countplot(data.total_words)


# In[467]:


# dropping rows with length 0
data = data.loc[data.total_words > 1,:]


# In[468]:


tweet_list = list(data.clean_text)
tweet_text = ' '.join(map(str, tweet_list))


# In[469]:


from nltk.tokenize import word_tokenize
from nltk.text import Text
from nltk.util import ngrams

tokens = word_tokenize(tweet_text)
t = Text(tokens)


# In[470]:


f, ax = plt.subplots(figsize=(20,15))
t.plot(30)

t.vocab()


# In[471]:


from nltk.util import ngrams
from nltk import FreqDist

bigram_freq = FreqDist(list(ngrams(t,2)))

f, ax = plt.subplots(figsize=(20,15))
bigram_freq.plot(30)


# In[472]:


sorted(bigram_freq)


# In[488]:


get_ipython().system('ipython nbconvert --to python extract_info.ipynb')

