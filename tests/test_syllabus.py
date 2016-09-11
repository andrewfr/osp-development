import unittest

from classifiers.SyllabusClassifier import SyllabusClassifier
from tools.pipeline import build_tables, build_data_set, print_statistics
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix

import numpy as np

class TestSyllabus(unittest.TestCase):
    def setUp(self):
        self.classifier = SyllabusClassifier("data/syllabusClassifier.pkl")

    def test_predictions(self):

        table, data_files, responses = build_tables("data/dev-test.csv", "documents/")

        training_files, testing_files, training_responses, testing_responses = \
                    train_test_split(data_files, responses, test_size = .25, random_state = 0)

        testing_data = build_data_set(testing_files,"documents/")
        predictions = [bool(self.classifier.is_syllabus(data)) for data in testing_data]

        correct_cm = np.array([[63,14], [33, 134]])
        cm = confusion_matrix(testing_responses, predictions)
        self.assertTrue((cm == correct_cm).all())

if __name__ == "__main__":
    unittest.main()


