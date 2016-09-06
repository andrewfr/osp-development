import json
import numpy as np
import nltk
import csv

from nltk.stem.porter import PorterStemmer
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import cross_val_score
from sample_list import samples

from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn import tree

import string

PREFIX = "../documents/"
RESULTS = "./results/"

stemmer = PorterStemmer()

ngram_ranges = [(1,1), (1,2), (1,3), (2,2), (2,3), (3,3)]
min_dfs = [0, .05, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0]

#ngram_ranges = [(2,4)]
#min_dfs = [.9, .2, .3]

class Analyzer(object):
    def __init__(self):
        self.isSyllabus_table = self.build_isSyllabus()
        self.responses = [self.isSyllabus_table[str(sample)] for sample in samples]
        self.syllabus_list = self.build_file_names(samples)

        self.training, self.testing, self.responses_training, self.responses_testing = \
        train_test_split(self.syllabus_list, self.responses, test_size = .25, random_state = 0)

    def stem_tokens(self, tokens, stemmer):
        stemmed = []
        for item in tokens:
            stemmed.append(stemmer.stem(item))
        return stemmed
                            
    def tokenize(self, text):
        new_tokens = []
        tokens = nltk.word_tokenize(text)
        new_tokens = [token for token in tokens if token not in set(string.punctuation) ]
        #stems = stem_tokens(new_tokens, stemmer)
        stems = new_tokens
        return stems 

    def build_isSyllabus(self):
        table = {}
        with open(PREFIX + "isSyllabus.csv") as fp:
            reader = csv.reader(fp)
            next(reader)
            for row in reader:
                document = row[0].replace("../documents/","").replace(".txt","")
                table[document] = int(row[1])
        return table

    def build_file_names(self, file_names):
        syllabus_files = []
        for sample in samples:
            syllabus_files.append(PREFIX + str(sample)  + ".txt")
        return syllabus_files

    def analyze(self, run_id, start, finish, min_df):

        run = "run " + str(start) + " " + str(finish) + " " + str(min_df)

        vectorizer = CountVectorizer(input='filename', 
                                     tokenizer=self.tokenize,
                                     min_df = min_df,
                                     ngram_range = (start, finish),
                                     stop_words = 'english',
                                     strip_accents='unicode')

        try:
            dtm_training = vectorizer.fit_transform(self.training)
        except ValueError:
            print("Run: %s Accuracy: %f Precision: %f Recall: %f F1: %f" % (run, -1, -1, -1, -1))
            return

        #print(vectorizer.get_feature_names())

        dtm_testing = vectorizer.transform(self.testing)

        dtm_training = dtm_training.toarray()
        dtm_testing = dtm_testing.toarray()
        classifier = DecisionTreeClassifier(criterion="entropy", max_depth=10, random_state=0).fit(dtm_training,
                                            self.responses_training)

        accuracy_scores = cross_val_score(classifier, dtm_training, self.responses_training, cv=10)
        precision_scores = cross_val_score(classifier, dtm_training, self.responses_training, cv=10, scoring="precision")
        recall_scores = cross_val_score(classifier, dtm_training, self.responses_training, cv=10, scoring="recall")
        f1_scores = cross_val_score(classifier, dtm_training, self.responses_training, cv=10, scoring="f1")

        mean_accuracy = np.mean(accuracy_scores)
        mean_precision = np.mean(precision_scores)
        mean_recall = np.mean(recall_scores)
        mean_f1 = np.mean(f1_scores)

        print(run_id + ".json")

        with open(RESULTS + run_id + ".json", "w") as fp:
            fp.write(json.dumps(vectorizer.get_feature_names()))

        print("Run_id: %s Run: %s Accuracy: %f Precision: %f Recall: %f F1: %f" % (run_id, run, mean_accuracy, mean_precision, mean_recall, mean_f1))

    def get_false_negatives(self, predicted):
        fp = []
        for i in range(0, len(predicted)):
            file_name = self.responses_testing[i].replace(".txt","").replace(PREFIX,"")
            if (self.is_syllabus[file_name] == '1' and predicted[i] == '0'):
                fp.append((file_name, int(self.is_syllabus[file_name]), int(predicted[i])))
        return fp

    def get_false_positives(self, predicted):
        fp = []
        for i in range(0, len(predicted)):
            file_name = self.responses_testing[i].replace(".txt","").replace(PREFIX,"")
            if (self.is_syllabus[file_name] == '0' and predicted[i] == '1'):
                fp.append((file_name, int(self.is_syllabus[file_name]), int(predicted[i])))
        return fp

def main():

    def make_id(start, finish, min_df):
        str_min_df = str(min_df).replace(".","-")
        return "experiment-" + str(start) + "-" + str(finish) + "-" + str_min_df 

    analyzer = Analyzer()

    for start, finish in ngram_ranges:
        for min_df in min_dfs:
            run_id = make_id(start, finish, min_df)
            results = analyzer.analyze(run_id, start, finish, min_df)


if __name__ == "__main__":
    main()
