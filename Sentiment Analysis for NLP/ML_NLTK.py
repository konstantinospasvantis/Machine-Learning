# -*- coding: utf-8 -*-
"""ML_NLTK_1st.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1u6T6833mVXQkvgqRKANAISsvLR-zKuqR
"""

#Importing libraries
import nltk
import numpy as np
from collections import Counter, defaultdict
import random
nltk.download('gutenberg')
from nltk.corpus import gutenberg
gutenberg.fileids()
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

#10 books from gutenberg (my choice)
list_of_books=['austen-persuasion.txt',
               'blake-poems.txt',
               'bryant-stories.txt',
               'burgess-busterbrown.txt',
               'carroll-alice.txt',
               'chesterton-thursday.txt',
               'milton-paradise.txt',
               'shakespeare-caesar.txt',
               'shakespeare-hamlet.txt',
               'shakespeare-macbeth.txt']
dict_of_words=dict()
#Specifying a dictionary with books as keys, and unique words and punctuaton marks as values
for book in list_of_books:
  dict_of_words[book]=np.unique(gutenberg.words(book))

##Tokenize words and sentences from the 10 books Ι picked
#Austen - Persuation
persuation_words=gutenberg.words('austen-persuasion.txt')
persuation_sentences=gutenberg.sents('austen-persuasion.txt')

#Blake - poems
poems_words=gutenberg.words('blake-poems.txt')
poems_sentences=gutenberg.sents('blake-poems.txt')

#Bryant - Stories
stories_words=gutenberg.words('bryant-stories.txt')
stories_sentences=gutenberg.sents('bryant-stories.txt')

#Burgess - Busterbrown
busterbrown_words=gutenberg.words('burgess-busterbrown.txt')
busterbrown_sentences=gutenberg.sents('burgess-busterbrown.txt')

#Caroll - Alice
alice_words=gutenberg.words('carroll-alice.txt')
alice_sentences=gutenberg.sents('carroll-alice.txt')

#Chesterton - Thursday
thursday_words=gutenberg.words('chesterton-thursday.txt')
thursday_sentences=gutenberg.sents('chesterton-thursday.txt')

#Milton - Paradise
paradise_words=gutenberg.words('milton-paradise.txt')
paradise_sentences=gutenberg.sents('milton-paradise.txt')

#Shakespeare - Ceasar
ceasar_words=gutenberg.words('shakespeare-caesar.txt')
ceasar_sentences=gutenberg.sents('shakespeare-caesar.txt')

#Shakespeare - Hamlet
hamlet_words=gutenberg.words('shakespeare-hamlet.txt')
hamlet_sentences=gutenberg.sents('shakespeare-hamlet.txt')

##Shakespeare - Macbeth
macbeth_words=gutenberg.words('shakespeare-macbeth.txt')
macbeth_sentences=gutenberg.sents('shakespeare-macbeth.txt')

#Words from each book stored in a list
sentences_list=[persuation_sentences, poems_sentences, stories_sentences, busterbrown_sentences, alice_sentences, thursday_sentences, paradise_sentences, ceasar_sentences, hamlet_sentences, macbeth_sentences]
books_list=['Austen - Persuation','Blake - Poems', 'Bryant - Stories' , 'Burgess - Busterbrown','Caroll - Alice','Chesterton - Thursday','Milton - Paradise','Shakespeare - Ceasar' ,'Shakespeare - Hamlet','Shakespeare - Macbeth']

#Creating a function that returns a double dictionary, to compute the probabilities of each bigram 
#For example, an instance of this dictionary could be {'The' : {'kid':0.02, 'boy': 0.12, ....},...}
#To achive this, we count the frequency of each word after another and storing it to dictionary.
#Next, we add all the frequencies of each word that follows the first word of each bigram, in order to divide the frequency of each biagram with this value.
#This is the probability for each bigram in a book.
def find_bigram_probabilities(list_of_sentences):
  b_model = defaultdict(lambda: defaultdict(lambda: 0))
  for sentence in list_of_sentences:
      for w1, w2 in nltk.bigrams(sentence, pad_right = True, pad_left = True):
        if w1==None or w2==None:
          pass
        else:
          b_model[w1][w2] += 1
  for w1 in b_model:
      total_count = float(sum(b_model[w1].values()))
      # If the total_count == 0 then pass, which means if the bigram does not exist, then it should skip it
      if total_count == 0:
          pass
      # Again if it does not exist assign the value 0 
      for w2 in b_model[w1]:
          if total_count == 0:
            b_model[w1][w2] = 0
          # If the brigram is not 0, then it calculates the probability
          else:
            b_model[w1][w2] /= total_count
  return b_model

#Similar to the function of probabilities for bigrams.
def find_trigram_probabilities(list_of_sentences):
  t_model = defaultdict(lambda: defaultdict(lambda: 0))
  for sentence in list_of_sentences:
    for w1, w2,w3 in nltk.trigrams(sentence, pad_right = True, pad_left = True):
      if w1==None or w2==None or w3==None:
        pass
      else:
        t_model[w1,w2][w3] += 1
  for w1_w2 in t_model:
      total_count = float(sum(t_model[w1_w2].values()))
      # If the total_count == 0 then pass, which means if the bigram does not exist, then it should skip it
      if total_count == 0:
          pass
      # Again if it does not exist assign the value 0 
      for w3 in t_model[w1_w2]:
          if total_count == 0:
              t_model[w1_w2][w3] = 0
          # If the brigram is not 0, then it calculates the probability
          else:
              t_model[w1_w2][w3] /= total_count
  return t_model

#Next, we build the model for creating random sentences. 
#Here we choose the start token to be the word 'the' , and the end token to be the typical dot '.'.
#To generate a random next word, we make use of the double dictionary we created. 
#For example, in the beggining we take the word 'the', and then we randomly choose one of the words that follows 'the' from the dictionary we created. 
#By saying randomly choose, we mean that we pick a word with the value of probability we calculated.
#Once the last token we generated was '.' , we stop generating new words and then we join the elements of the list in one sentence.
def print_sentences_for_bigrams(bigram_model):
    # Choose a seed word to start the sentence
    seed_word = 'the'
    # Initialize an empty list to hold the generated words
    generated_words = [seed_word]
    # Keep generating words until the sentence reaches a stopping point
    while True:
      # Get the list of possible next words and their probabilities
      next_words = bigram_model[generated_words[-1]]
      if len(next_words)==0:
        break
      else:
        # Choose the next word by sampling from the list of possibilities
        next_word = random.choices(list(next_words.keys()), weights=next_words.values(), k=1)[0]
        if next_word==None:
          pass
        else:
          generated_words.append(next_word)

        # If the next word is a period, stop generating words
        if next_word == ".":
          break

    # Join the generated words into a single string to form the sentence
    sentence = " ".join(generated_words)
    return sentence

#Similar to the function that prints sentences for bigrams
def print_sentences_for_trigrams(trigram_model):
    # Choose a seed word to start the sentence
    # Initialize an empty list to hold the generated words
    generated_words = ['and','the']
    # Keep generating words until the sentence reaches a stopping point
    while True:
      # Get the list of possible next words and their probabilities
      next_words = trigram_model[generated_words[-2],generated_words[-1]]
      if len(next_words)==0:
        break
      else:
        # Choose the next word by sampling from the list of possibilities
        next_word = random.choices(list(next_words.keys()), weights=next_words.values(), k=1)[0]

        # Add the next word to the generated words list
        generated_words.append(next_word)

        # If the next word is a period, stop generating words
        if next_word == ".":
          break

    # Join the generated words into a single string to form the sentence
    sentence = " ".join(generated_words)
    return sentence

#Printing 10 sentences for each book using bigrams
print('10 random sentences using bigrams for each book :')
for i in range(10):
  print('10 random sentences using bigrams for '+ str(books_list[i]) + ':')
  for j in range(1,11):
    print('Sentece ' , j , ": ",print_sentences_for_bigrams(find_bigram_probabilities(sentences_list[i])))

#Printing 10 sentences for each book using trigrams
print('10 random sentences using trigrams for each book :')
for i in range(10):
  print('10 random sentences using trigrams for '+ str(books_list[i]) + ':')
  for j in range(1,11):
    print('Sentece ' , j , ": ",print_sentences_for_trigrams(find_trigram_probabilities(sentences_list[i])))

"""# PART 2 (REVIEWS)"""

#Here we download the necessary modules, in order to load movie_revies.
import nltk
from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.svm import SVC
from sklearn import model_selection
nltk.download('movie_reviews')
#Have a glimpse of the words that exists in all reviews.
movie_reviews.words()
#We create a frequency distribution for all of the words.
all_words = nltk.FreqDist(movie_reviews.words())
#We choose only the 4000 most common words.
feature_vector = list(all_words)[:4000]
# Document is a list of (words of review, category of review)
#We have a list of tuples. The first element of each tuple is a list that contains every word contained in a review, and the second element contains the class of each review.
document = [(movie_reviews.words(file_id),category) for file_id in movie_reviews.fileids() for category in movie_reviews.categories(file_id)]
#we define a function that finds the features
def find_feature(word_list):
  # Initialization
   feature = {}
   # 'for' loop to find the features. ‘True’ is assigned if word in feature_vector can also be found in review. Otherwise ‘False’
   for x in feature_vector:
    feature[x] = x in word_list
   return feature

# Feature_sets stores the ‘feature’ of every review
feature_sets = [(find_feature(word_list),category) for (word_list,category) in document]

#Here we split the feature sets into train and test data.

train_set,test_set = model_selection.train_test_split(feature_sets,test_size = 0.25,random_state=1)

#And here we train the Naive Bayes model in order to classify the reviews from our test set.
classifier = nltk.classify.NaiveBayesClassifier.train(train_set)
accuracy = nltk.classify.accuracy(classifier, test_set)
print('Naive Bayes Classifier Accuracy : {}'.format(accuracy))
#We can see that the accuracy is pretty high, even if we took only 4000 words out of 39768.