import codecs
import json
import numpy as np
import csv

from sklearn.externals import joblib
from sklearn.cross_validation import train_test_split
from sklearn.externals import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report


PREFIX = "../documents/"

def build_tables(file_name, prefix):
    table = {}
    data = []
    responses = []
    with open(file_name) as fp:
        reader = csv.reader(fp)
        next(reader)
        for row in reader:
            document = row[0].replace(prefix,"").replace(".txt","")
            table[document] = int(row[1])
            data.append(document)
            responses.append(int(row[1]))
    return table, data, responses

def build_file_names(self, file_names, prefix):
    syllabus_files = []
    for sample in samples:
        syllabus_files.append(prefix + str(sample)  + ".txt")
    return syllabus_files

def build_data_set(data_files, prefix):
    file_set = []
    for file_name in data_files:
        file_name = prefix + str(file_name)  + ".txt"
        text = get_text(file_name)
        file_set.append(text)
    return file_set

def build_pipeline(parameters):
    pipeline = Pipeline([('vect', CountVectorizer(input='content',
                                                  decode_error = 'ignore',
                                                  min_df = 0.05,
                                                  ngram_range = (2,3),
                                                  stop_words="english",
                                                  strip_accents='unicode')),
                         ('clf', DecisionTreeClassifier(criterion="entropy", max_depth=10, random_state=0))])
    return pipeline

def get_text(file_name):
    with codecs.open(file_name, encoding="utf-8") as fp:
         text = fp.read()
    return text

def get_metrics(classifier, data, responses):
    accuracy_scores = cross_val_score(classifier, data, responses, scoring="accuracy", cv=5)
    precision_scores = cross_val_score(classifier, data, responses, cv=5, scoring="precision")
    recall_scores = cross_val_score(classifier, data, responses, cv=5, scoring="recall")
    f1_scores = cross_val_score(classifier, data, responses, cv=5, scoring="f1")
    mean_accuracy = np.mean(accuracy_scores)
    mean_precision = np.mean(precision_scores)
    mean_recall = np.mean(recall_scores)
    mean_f1 = np.mean(f1_scores)
    return mean_accuracy, mean_precision, mean_recall, mean_f1

def print_statistics(predictions, responses):
    cm = confusion_matrix(responses, predictions)
    print(np.mean(predictions == responses))
    print(cm)
    print(classification_report(responses, predictions))
    return

def save_pipeline(pipeline, file_name):
    joblib.dump(pipeline, file_name, compress=1)

def test_syllabus_classifier(data, responses):
    testing_data = build_data_set(testing_files)

def main():
    table, data_files, responses = build_tables("../data/dev-test.csv", PREFIX)
    training_files, testing_files, training_responses, testing_responses = \
                    train_test_split(data_files, responses, test_size = .25, random_state = 0)

    training_data = build_data_set(training_files, PREFIX)
    pipeline = build_pipeline(None)
    training_data = pipeline.fit_transform(training_data, training_responses)
    save_pipeline(pipeline, "syllabusClassifier.pkl")   


if __name__ == "__main__":
    main()
