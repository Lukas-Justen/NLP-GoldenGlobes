import nltk
import itertools
import gensim
import random
import src.kb_constant as kb_constant
from src.wikidata_connector import WikidataConnector
from nltk import TweetTokenizer, word_tokenize, Text, FreqDist, ngrams
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.corpus import words


class Chunker:

    def __init__(self):
        self.word_dict = dict.fromkeys(words.words() , 1)
        self.nominee_keys = kb_constant.nominee_keywords.split("|")
        self.presenter_keys = kb_constant.presenter_keywords.split("|")

    def detector(self,text_string, find_words):
      try:
        text_string = text_string.lower()
        for each_word in text_string.split():
            if each_word in find_words:
                return True
        return False
      except:
          return False
    def extract_chunks(self,text_string, chunker):
      try:
        # Get grammatical functions of words
        tagged_sents = nltk.pos_tag_sents(nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(text_string))

        # Make chunks from the sentences, using grammar. Output in IOB.
        all_chunks = list(itertools.chain.from_iterable(nltk.chunk.tree2conlltags(chunker.parse(tagged_sent)) for tagged_sent in tagged_sents))

        # Join phrases based on IOB syntax.
        candidates = [' '.join(w[0] for w in group) for key, group in itertools.groupby(all_chunks, lambda l: l[2] != 'O') if key]

        if candidates != []:
            candidates[0] = ' '.join([w for w in word_tokenize(candidates[0]) if w in self.word_dict])
            nominee_mentioned = self.detector(text_string,self.nominee_keys) #['nominate','nominates','nominated','nominating','nomination','nominee','nominees']
            presenter_mentioned = self.detector(text_string,self.presenter_keys) #['presented','presenting','presents','presenters','presenter','announce','announces','announced']
            return [nominee_mentioned, presenter_mentioned, candidates[0]]
        else:
            return 'N/a'
      except:
            return 'N/a'
    def extract_noun_pattern(self,series):

        chunker = nltk.RegexpParser("""Chunk: {<NN.?><NN.?|VB.?><NN.?>+}""")
        text_string = series['clean_text']
        #text_string = text_string.lower()

        return self.extract_chunks(text_string, chunker)

    def extract_adjective_pattern(self,series):

        chunker = nltk.RegexpParser("""Chunk: {<JJ.?|RB.?><JJ.?|NN.?|VB.?><IN.?>?<DT?>?<NN.?><JJ.?|NN.?>?<CC.?|NN.?>?<JJ.?|NN.?>?}""")
        text_string = series['clean_text']
        #text_string = text_string.lower()

        return self.extract_chunks(text_string, chunker)

    def extract_adverb_pattern(self,series):

        chunker = nltk.RegexpParser("""Chunk: {<RB.?> <NN.?> <IN>? <DT>? <CC>? <NN.?>+ <IN>? <DT>? <VB.?>? <NN.?|JJ.?> <NN.?>+ <CC>? <JJ>? <IN>? <DT>? <NN.?>? <VB.?>? <IN>? <NN.?>?}""")
        text_string = series['clean_text']
        #text_string = text_string.lower()

        return self.extract_chunks(text_string, chunker)

    def extract_wrapper(self,series):

       try:
        text_string = series['clean_text']

        if not 'best' in text_string.split():
            return 'N/a'

        wrap1 = self.extract_adjective_pattern(series)
        if wrap1 != 'N/a':
            return wrap1

        wrap2 = self.extract_adverb_pattern(series)
        if wrap2 != 'N/a':
            return wrap2

        return 'N/a'#self.extract_noun_pattern(series)

       except:
           return 'N/a'
    def fuzz_(self,catg_string, catg_list):
      try:
        string_list = catg_string.split()
        string_len = len(string_list)
        best_match = 0
        best_key = ''

        for key in catg_list:
            key = key.lower().split()
            count = 0
            for word_ in string_list:
                if word_ in key:
                    count += 1
            print((count / string_len)*100)
            if  (count / string_len)*100 > 90 and (string_len-1 == len(key) or string_len+1 == len(key)):
                best_match = (count / string_len)*100
                best_key = ' '.join(key)

        return best_key
      except:
          return ''

    def pick_categories(self,data):

        top_categories = data['categorie'].value_counts()[:40].keys().tolist()

        for each_categorie in top_categories:
            categorie_list = top_categories.copy()
            categorie_list.remove(each_categorie)
            twin_categorie = self.fuzz_(each_categorie, categorie_list)
            if twin_categorie != '':
               top_categories.remove(twin_categorie)

        return top_categories