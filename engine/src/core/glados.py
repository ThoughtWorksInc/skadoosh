import nltk, re, pprint
import os
import csv

CURR_PATH = os.path.dirname(__file__)

def extract_feature_from_doc(document):
  features = []
  for (text,category) in document:
    sent_features = extract_feature(text)
    features.append((sent_features, category))
  return features

def extract_feature(text):
  sentences = nltk.sent_tokenize(text)
  sentences = [nltk.word_tokenize(sent) for sent in sentences]
  sentences = [nltk.pos_tag(sent) for sent in sentences]
  return getNN(sentences)

def getNN(sentences):
   sent_keys = []
   for sent in sentences:
      keys = [x for (x,n) in sent if n=='NN' or n=='VBN']
      if len(keys) == 0:
        keys = [x for (x,n) in sent]
      sent_keys.extend(keys)
   return {'keywords': '|'.join(sent_keys)}

def get_traning_content():
  test_doc = os.path.join('res/training.txt')
  with open(test_doc, 'r') as content_file:
    lines = csv.reader(content_file,delimiter='|')
    return [x for x in lines]

if __name__ == '__main__':
  document = get_traning_content()
  features = extract_feature_from_doc(document)
  print('\n'.join([str(x) for x in features]))

  train_set = features
  classifier = nltk.NaiveBayesClassifier.train(train_set)
  print(classifier.classify(extract_feature('Tell my account balance.')))
  