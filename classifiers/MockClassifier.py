import sys
import random

class MockSyllabusClassifier(object):
    """
    emulates baseline estimate
    """
    def __init__(self, fileName):
        pass


    def is_syllabus(self, text):
        """ determine if a document is a syllabus

        Args:
            text: a string representing a document

        return:
            boolean True is a syllabus. False not a syllabus
        """
        i = random.randint(1,10)
        return(i in range(1,8))

