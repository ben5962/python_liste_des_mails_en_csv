# je veux un objet mail qui me dise
# questions necessitant acces à un seul champ:
# - si un mail contient une pj de nom de fichier 'untel'
# - si un mail contient une pj de type 'untel'
# - le from
# - le sujet
# - la date du mail
# - le nom du fichier dont provient l objet mail
# questions necessitant acces à plusieurs champs: 
# - la liste des pj par nom et type


# comme toutes ces questions sont déjà résolues par le module mail,
# ecrire une fonction enveloppante pour les pj et pour les mails
import email
from email import policy
from email.parser import BytesParser
from email.iterators import walk
from dateutil.parser import *
from io import StringIO
class Objet_mail(email.message.EmailMessage):
    #class Objet_mail(email.message.EmailMessage):
    #AttributeError: 'Objet_piece_jointe' object has no attribute '_headers'
    #class Objet_mail(email.parser.BytesParser):
    #AttributeError: 'Objet_piece_jointe' object has no attribute '_headers'

    def __init__(self,nom_fichier_mail):
        self.setName(nom_fichier_mail)
        self.setConteneurMail()
        self.setFromToDateSubject()
        self.setListePiecesJointes()
        self.setListeNomFichiersPiecesJointes()

    # set / get 

    def setName(self,nom_fichier_mail):
        if nom_fichier_mail.endswith('.eml'):
            self.nom_fichier_mail = nom_fichier_mail
        else:
            raise ValueError("le nom de fichier doit se terminer par eml: {}".format(nom_fichier_mail))


    
    
    def setConteneurMail(self):
        with open(self.nom_fichier_mail, 'rb') as fp:
            self.conteneurMail = BytesParser(policy=policy.default).parse(fp, headersonly=False)

    def setFromToDateSubject(self):
        #self.isfrom = self.conteneurMail.get_all('From',None)
        self.isfrom = self.conteneurMail.get('From',None)
        #self.isto = self.conteneurMail.get_all('To',None)
        self.isto = self.conteneurMail.get('To',None)
        self.isdate = parse(self.conteneurMail.get('Date',None))
        self.issubject = self.conteneurMail.get('Subject',None)

    
        

    def setListePiecesJointes(self):
        #http://blog.magiksys.net/parsing-email-using-python-content
        #https://www.ianlewis.org/en/parsing-email-attachments-python
        # https://docs.python.org/3/library/email.message.html#email.message.EmailMessage.get_content_type
        self.liste_pieces_jointes = []
        compteur_piece_jointe = 1
        for part in self.conteneurMail.iter_attachments():
            non_nul_si_piece_jointe = cree_Objet_Piece_Jointe(part,self, compteur_piece_jointe)
            if non_nul_si_piece_jointe:
                self.liste_pieces_jointes.append(non_nul_si_piece_jointe)
                compteur_piece_jointe = compteur_piece_jointe + 1

    def setListeNomFichiersPiecesJointes(self):
        if self.liste_pieces_jointes:
            self.liste_noms_fichiers_pieces_jointes = []
            from module_utilitaire_fichier import clean_windows_filename_string
            for pj in self.liste_pieces_jointes:
                self.liste_noms_fichiers_pieces_jointes.append(clean_windows_filename_string(pj.getFileName()))


    # getters 


    def getName(self):
        return self.nom_fichier_mail

    def getDate(self):
        return self.isdate

    def getSubject(self):
        return self.issubject

    def getFrom(self):
        return self.isfrom

    # utilitaires

    def getAttachmentCount(self):
        return len(self.liste_pieces_jointes)

    def getAllAttachmentFilenames(self):
        if self.liste_noms_fichiers_pieces_jointes:
            return self.liste_noms_fichiers_pieces_jointes
        else:
            return []

    def getAllSearchableMailheaderKeyNames(self):
        return self.conteneurMail.keys()

    def getNormalizedName(self):
        import re
        filename_with_unauthorized_characters = ''.join([self.getDate().isoformat(sep=' '),
                        self.getSubject(),
                        #self.getFrom(),
                        re.search(r'\<(.*)\>', self.getFrom()).group(1),
                        'has ' + str(self.getAttachmentCount()) + ' pj',
                        '_'.join(self.getAllAttachmentFilenames()),
                        '.eml'])
        from module_utilitaire_fichier import clean_windows_filename_string
        
        return clean_windows_filename_string(filename_with_unauthorized_characters)
        
        

def cree_Objet_Piece_Jointe(mailpart,mailinstance,numeropiecejointe):
    class Objet_piece_jointe(object):
    #class Objet_piece_jointe(email.message.EmailMessage):
    #class Objet_piece_jointe(email.message.MIMEPart):
        def __init__(self,mailpart,mailinstance):
            self.mailinstance = mailinstance
            self.numeropiecejointe = numeropiecejointe
            self.setRawData(mailpart)
            self.parseAttachment(mailpart,mailinstance)


        #setters
        def setRawData(self,mailpart):
            self.file_data = mailpart.get_content()
            #self.attachment = StringIO(self.file_data)
            #TypeError: initial_value must be str or None, not bytes


            
            

            
        def parseAttachment(self,mailpart,mailinstance):
            #bug noname (30).eml:
            # il a deux pieces jointes
            # il a un nom de fichier trop long qui utilise la continuation de ligne
            # file*1*
            track_filename_in_disposition = ["filename"," filename"]
            track_filename_in_content = ['name']
            #import pdb; pdb.set_trace()
            self.content_disposition = mailpart.get("Content-Disposition", None)
            if self.content_disposition:
                self.mailinstance = mailinstance
                dispositions = self.content_disposition.strip().split(";")
                #print(dispositions)
                
                if not bool(self.content_disposition and (dispositions[0].lower() == "attachment"
                                                          or dispositions[1].split('=')[0] in track_filename_in_disposition
                                                          or mailpart.get('Name',None))):
                                raise ValueError("le champ content_disposition {}n a pas la forme attendue, pas plus que name pour sauver la mise {} pour la piece jointe numero {} ".format(self.content_disposition,mailpart.get('Name',None),self.numeropiecejointe))
                self.content_type = mailpart.get_content_type()
                self.size = len(self.file_data)
                self.name = None
                self.create_date = None
                self.mod_date = None
                self.read_date = None
                # traiter filename separement
                #http://blog.magiksys.net/parsing-email-using-python-content get_ilename
                    
                self.name = mailpart.get_filename(None)   
                for param in dispositions[1:]:
                    name,value = param.split("=")
                    name = name.lower()
                    #dbg_print(name,)

                    if name == "filename":
                        if not self.name:
                            self.name = value # todo strip name
                    #shitty hack seing what domo mailserver spits
                    elif name == " filename":
                        if not self.name:
                            self.name = value #todo strip name
                    elif name == "create-date":
                        self.create_date = parse(value)  
                    elif name == "modification-date":
                        self.mod_date = parse(value) 
                    elif name == "read-date":
                        self.read_date = parse(value)
                # correction des parametres necessaires
                # attachment has a name
                if not self.name:
                    if mailpart.get('name',None):
                        self.name = mailpart.get('name',None)
                        print(self.name)
                    else:
                        # pas la peine de conttinuer il y a une couille
                        raise ValueError("la piece jointe doit avoir un nom")
                # attachment has a date
                if self.create_date:
                    print("create_date vaut: {}".format(self.create_date))
                if not self.create_date:
                    self.create_date = mailinstance.getDate()
                    print("create exite pa . je ui attribue: {}".format(self.create_date))
                
                self.is_attachment = True
                
            else:
                self.is_attachment = False

        #getters

        def getFileName(self):
            return self.name

        def getFileType(self):
            return self.content_type

        #utilitaires
            

        def getFile(self):
            dest = self.getFileName()
            with open(dest, 'wb') as g:
                g.write(self.file_data)

        
                
            

        

    # fin de la décla de la classe Piece_jointe

    # execution de la fonction cree_piece_jointe:    
    pj = Objet_piece_jointe(mailpart,mailinstance)
    if pj.is_attachment:
        return pj
    else:
        return None
                        
            

















































            
            
            
        
            
