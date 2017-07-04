import unittest
import email

class TestEmail(unittest.TestCase):
    """from
https://docs.python.org/3/library/email.message.html#module-email.message
"""

    def testParseEmailfromBinaryfile(self,fichier):
        fp = open(fichier,'rb')
        e = email.message_from_binary_file(fp)
        verite = True if e.__len__() else False
        self.assertTrue(verite)
        
