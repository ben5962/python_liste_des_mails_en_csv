'''
Created on 2 juil. 2017

@author: Utilisateur
'''

class EmailParser(object):
    '''
    classdocs 
    parse les emails indépendamment de la classe utilisée
    '''


    def __init__(self, fichier=None):
        '''
        Constructor
        '''
        self.setFichier(fichier) if fichier is not None else self.setFichier("")
        
    def setFichier(self,fichier):
        self.fichier = fichier
    
    def display_email_header_from_email(self):
        
        with open(self.getFichier(),'rb') as f:
            import email
            objet_emaildotmessage = email.message_from_binary_file(f)
            #email.message.EmailMessage.items()
            print(objet_emaildotmessage.EmailMessage.items())
        
        
