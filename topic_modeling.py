import gensim
import pandas as pd
from gensim import corpora

data = pd.read_csv("../data/cleaned_gg2013.csv")

print("Build dictionary:")
# Build the dictionary and the term matrix for the LDA run
doc_clean = [str(row).split() for row in data["clean_text"][:10000]]
dictionary = corpora.Dictionary(doc_clean)
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
print("Done\n")

print("Set up LDA Model:")
# Build the LDA model
Lda = gensim.models.ldamodel.LdaModel
ldamodel = Lda(doc_term_matrix, num_topics=60, id2word=dictionary, passes=50)
print("Done\n")

print("Results:")
# Print out the results of the LDA run
for i in ldamodel.print_topics(num_topics=60, num_words=10):
    print(i)
print("Done\n")
