import unittest
import email

class TestEmail(unittest.TestCase):
    """from
https://docs.python.org/3/library/email.message.html#module-email.message
"""

    def ParseEmailfromBinaryfile(self,fichier):
        with open(fichier,'rb') as fp:
            e = email.message_from_binary_file(fp)
            verite = True if e.__len__() else False
            return verite

    def TestParseEmailFromBinaryFile(self):
        self.assertTrue(self.ParseEmailfromBinaryfile('exemple.eml'))
        
    
