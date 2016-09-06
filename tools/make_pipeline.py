import re
import sys
import numpy as np
import nltk
import csv

from sklearn.externals import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cross_validation import train_test_split
from master_samples import samples

PREFIX = "../documents/"

def build_isSyllabus():
    table = {}
    with open("master.csv") as fp:
        reader = csv.reader(fp)
        next(reader)
        for row in reader:
            document = row[0].replace("../documents/","").replace(".txt","")
            table[document] = int(row[1])
    return table

def build_file_names(file_names):
    syllabus_files = []
    for sample in samples:
        syllabus_files.append(PREFIX + str(sample)  + ".txt")
    return syllabus_files

def main():
    isSyllabus_table = build_isSyllabus()
    responses = [isSyllabus_table[str(sample)] for sample in samples]
    syllabus_list = build_file_names(samples)

    training, testing, responses_training, responses_testing = train_test_split(
                    syllabus_list, responses, test_size = .25, random_state = 0)

    pipeline = Pipeline([('vect', CountVectorizer(input='filename', 
                                                  decode_error = 'ignore',
                                                  min_df = 0.05,
                                                  ngram_range = (2,3),
                                                  strip_accents='unicode')),
                         ('clf', DecisionTreeClassifier(criterion="entropy", max_depth=10, random_state=0))])
                    
    pipeline.fit_transform(training, responses_training)
    joblib.dump(pipeline, 'syllabusClassifier.pkl',compress=1)


if __name__ == "__main__":
    main()
