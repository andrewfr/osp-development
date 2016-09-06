import sys
from sklearn.externals import joblib

class SyllabusClassifier(object):
    def __init__(self, fileName):
        """Stub for Syllabus classifiers

        Args:
            fileName : file name of pk1 and associated files 

        """
        self.pipeline = joblib.load(fileName)


    def is_syllabus(self, text):
        """ determine if a document is a syllabus

        Args:
            text: a string representing a document

        return:
            boolean True is a syllabus. False not a syllabus
        """
        text = unicode(text)
        self.pipeline.set_params(vect__input='content')
        transformed = self.pipeline.transform(text)
        prediction = self.pipeline.predict(transformed)
        return(prediction)


def main():
    reload(sys)
    sys.setdefaultencoding('utf8')

    with open("../documents/9943.txt") as fp:
        text = fp.read()

    classifier = SyllabusClassifier("syllabusClassifier.pkl")
    print(classifier.is_syllabus(text))

if __name__ == "__main__":
    main()
