import sys
from sklearn.externals import joblib

class SyllabusClassifier(object):
    def __init__(self, fileName):
        """Stub for Syllabus classifiers

        Args:
            fileName : pickle file 

        """
        self.pipeline = joblib.load(fileName)


    def is_syllabus(self, text):
        """ determine if a document is a syllabus

        Args:
            text: a string representing a document

        return:
            boolean True is a syllabus. False not a syllabus
        """

        return self.pipeline.predict([text])


def main():
    reload(sys)
    sys.setdefaultencoding('utf8')

    with open("../documents/9943.txt") as fp:
        text_1 = fp.read()

    with open("../documents/34657.txt") as fp:
        text_2 = fp.read()

    classifier = SyllabusClassifier("syllabusClassifier.pkl")
    assert classifier.is_syllabus(text_1) == True

    assert classifier.is_syllabus(text_2) == False
    
if __name__ == "__main__":
    main()
