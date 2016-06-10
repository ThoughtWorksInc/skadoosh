import nltk, re, pprint

def ie_preprocess(document):
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences


if __name__ == '__main__':
    test_doc = 'test_doc.txt'
    with open(test_doc, 'r') as content_file:
        document = content_file.read()
    sentences = ie_preprocess(document)
    print(sentences)