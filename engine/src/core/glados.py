import nltk, re, pprint
import sys
import os
import csv
import argparse

CURR_PATH = os.path.dirname(__file__)

def extract_feature_from_doc(document):
  features = []
  for (text,category,answer) in document:
    sent_features = extract_feature(text)
    # features.append((sent_features, category))
    features.append((sent_features, answer))
  return features

def extract_feature(text):
  sentences = nltk.sent_tokenize(text)
  sentences = [nltk.word_tokenize(sent) for sent in sentences]
  sentences = [nltk.pos_tag(sent) for sent in sentences]
  return get_feature_set(sentences)

def get_feature_set(sentences):
   sent_keys = []
   for sent in sentences:
      keys = [x for (x,n) in sent if n=='NN' or n=='VBN']
      if len(keys) == 0:
        keys = [x for (x,n) in sent]
      sent_keys.extend(keys)
   return {'keywords': '|'.join(sent_keys)}

def get_traning_content(filename):
  test_doc = os.path.join(filename)
  with open(test_doc, 'r') as content_file:
    lines = csv.reader(content_file,delimiter='|')
    return [x for x in lines]

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
  
def train_and_get_classifer(training_set_filename):
  document = get_traning_content(training_set_filename)  
  train_set = extract_feature_from_doc(document)
  log('\n'.join([str(x) for x in train_set]))
  classifier = nltk.NaiveBayesClassifier.train(train_set)
  return classifier
  
if __name__ == '__main__':
  scanArgs()
  account_info = {
    'name': 'John',
    'balance': 323710.38,
    'account_no': 12900989124,
    'phone': 73710203
  }
  
  classifier = train_and_get_classifer('res/training.txt')
  ans = classifier.classify(extract_feature('Tell my account balance.'))
  if len(ans) > 0:
    print(ans % account_info)
  else:
    print("Unable to understand your request. Please try again")
  # print(classifier.show_most_informative_features(5))
  