import nltk, re, pprint
import sys
import os
import csv
import argparse
from nltk.stem.snowball import SnowballStemmer

CURR_PATH = os.path.dirname(__file__)
module_path = os.path.abspath(os.path.join(CURR_PATH, '..'))
sys.path.append(module_path)

from core.utils import *

class Glados(object):
  def __init__(self,traning_filename=None,test_filename=None):
    if isEmpty(traning_filename):
      traning_filename = os.path.join(CURR_PATH, 'res/training.txt')
    if isEmpty(test_filename):
      test_filename = os.path.join(CURR_PATH, 'res/test_data.txt')
    self.traning_filename = traning_filename
    self.test_filename = test_filename
    self.stemmer = SnowballStemmer("english")
    self.classifier = self.train_and_get_classifer(traning_filename, test_filename)
  
  """
  Public api
  input: user question text
  output: answer
  """
  def get_help(self, question):
    features = self.extract_feature(question)
    answer = self.classifier.classify(features)
    prob = self.classifier.prob_classify(features)
    response = dict(question=question,answer=answer,probility=prob.prob(answer))
    return response
      
  def train_and_get_classifer(self, training_set_filename, test_set_filename):
    training_data = self.get_traning_content(training_set_filename)
    train_set = self.extract_feature_from_doc(training_data)
    training_data_length = len(training_data)

    test_data = self.get_traning_content(test_set_filename)
    test_set = self.extract_feature_from_doc(test_data)

    log('\n'.join([str(x) for x in train_set]))

    classifier = nltk.NaiveBayesClassifier.train(train_set)
    classifier_name = type(classifier).__name__
    training_set_accuracy = nltk.classify.accuracy(classifier, train_set)
    test_set_accuracy = nltk.classify.accuracy(classifier, test_set)
    # print(classifier.most_informative_features())

    output_file = open(os.path.join(CURR_PATH,"res/accuracy.txt"), "a")
    output_file.write("\n%s\t\t%s\t\t\t%.8f\t\t%.8f" % (classifier_name, training_data_length, training_set_accuracy, test_set_accuracy))
    output_file.close()

    return classifier
    
  def extract_feature_from_doc(self, document):
    features = []
    for (text,category,answer) in document:
      sent_features = self.extract_feature(text)
      # features.append((sent_features, category))
      features.append((sent_features, answer))
    return features

  def extract_feature(self, text):
    sentences = nltk.sent_tokenize(text)
    words = [nltk.word_tokenize(sent) for sent in sentences]
    tags = [nltk.pos_tag(sent) for sent in words]
    sent_keys = self.extract_keys(tags)
    stemmed_words = [self.stemmer.stem(x) for x in sent_keys]
    return self.get_feature_set(stemmed_words)

  def extract_keys(self, sentences):
    sent_keys = []
    for sent in sentences:
        keys = [x for (x,n) in sent if n=='NN' or n=='VBN']
        if len(keys) == 0:
          keys = [x for (x,n) in sent]
        sent_keys.extend(keys)
    return sent_keys

  def get_feature_set(self, sent_keys):
    return {'keywords': '|'.join(sent_keys)}

  def get_traning_content(self, filename):
    test_doc = os.path.join(filename)
    with open(test_doc, 'r') as content_file:
      lines = csv.reader(content_file,delimiter='|')
      res = [x for x in lines if len(x) == 3]
      return res

DEBUG = False
def log(msg):
  global DEBUG
  if DEBUG == True: print(msg)

def scanArgs():
  global DEBUG
  parser = argparse.ArgumentParser(description='Glados virtual help engine')
  parser.add_argument('-d', '--debug', action='store_true', help='Enable debug log output')
  args = parser.parse_args()
  DEBUG = args.debug
  
if __name__ == '__main__':
  scanArgs()
  account_info = {
    'name': 'John',
    'balance': 323710.38,
    'account_no': 12900989124,
    'phone': 73710203
  }
  
  glados = Glados()
  ans = glados.get_help('Tell my account balance.')
  if len(ans) > 0:
    print(ans % account_info)
  else:
    print("Unable to understand your request. Please try again")
  # print(classifier.show_most_informative_features(5))
  print(glados.get_help('what different credit cards you provide?'))
  