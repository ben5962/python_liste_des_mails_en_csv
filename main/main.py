'''
Created on 2 juil. 2017

@author: Utilisateur
'''

def run():
    import fileutils.parcours_repertoire as p
    objet_parcours = p.Parcours(glob="*.eml", root="../eml/")
    print(objet_parcours.getFirstFilePath())
    import parse_email.parse_email as ep
    objet_email_parser =  ep.EmailParser(fichier=objet_parcours.getFirstFilePath())
    objet_email_parser.display_email_header_from_email()
    
    

if __name__ == '__main__':
    run()