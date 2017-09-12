import email
import email
import glob
from email import policy
from email.parser import BytesParser
from email.iterators import walk
from dateutil.parser import *
from module_objet_mail import *
files = glob.glob('*.eml') # returns list of files
format_souhaite = ('Message-ID','Date','Subject','From','Content-Type')











# done  : parser_date avec dateutils,
# done ajouter chp possede pj, type pj et
# ttodo: evtl l extraire le parser et en deduire les dates de debut et de fin
# todo: amelio"rer code (sepa flux exe de comment sur base iens sites internet de calendar)

#https://www.saltycrane.com/blog/2008/01/how-to-use-args-and-kwargs-in-python/
def parcourir(f, format_souhaite=None, **kwargs):
        for fichier in files:
            with open(fichier, 'rb') as fp:
                msg = BytesParser(policy=policy.default).parse(fp, headersonly=True)
                print("dan parcourir appel de f avec pour param:{}".format(repr(msg) + fichier + repr(format_souhaite) + repr(kwargs)))
                f(msg = msg, format_souhaite = format_souhaite, nom_fichier = fichier, **kwargs)

def afficher_un(msg, format_souhaite=None):
    return dict(zip(format_souhaite,map(msg.get,format_souhaite)))


def rechercher_un(msg):
    return msg.keys()
    
def afficher_fonctionnel():
    return parcourir(f=afficher_un, format_souhaite=format_souhaite)

def rechercher_fonctionnel():
    return parcourir(f=rechercher_un)

def rechercher_possible_pj_un(msg,format_souhaite=None):
    for part in msg.walk():
        yield dir(part)


def rechercher_possible_pj_fonctionel():
    return next(parcourir(f=rechercher_possible_pj_un, format_souhaite=format_souhaite))




            
def afficher():
    for fichier in files:
        with open(fichier, 'rb') as fp:
            msg = BytesParser(policy=policy.default).parse(fp, headersonly=True)
            d = dict(zip(format_souhaite,map(msg.get,format_souhaite)))
            print(d)
            

def rechercher():
    for fichier in files:
        with open(fichier, 'rb') as fp:
            msg = BytesParser(policy=policy.default).parse(fp, headersonly=True)
            yield msg.keys()
            
    
def piece_jointe():
    for fichier in files:
        #iter_attachments()!
        print(fichier)
        with open(fichier, 'rb') as fp:
            msg = BytesParser(policy=policy.default).parse(fp)
            print(type(msg))
            for part in msg.walk():
                print(type(part))
                pj_potentielle = dict(
                    zip(['fichier_mail','type_de_sous_partie',
                         'organisation_sous_partie',
                         'type_fichier',
                         'nom_fichier'
                         ]
                        
                        ,
                        [fichier, part.get('Content-Type'),
                         part.get('Content-Disposition'),
                         None if not part.get('Content-Disposition') else part.get('Content-Type').split(';')[0],
                         None if not part.get('Content-Disposition') else part.get('Content-Disposition').split(';')[1].split('=')[1].replace("'","").strip()
                          
                           
                         ]
                        )
                    )
                if pj_potentielle['nom_fichier'] is not None:
                        #filtrer : seulement les pj
                        print(pj_potentielle['nom_fichier'])
                        #extraire pj
                        dest = part.get('Content-Disposition').split(';')[1].split('=')[1].replace("\"","").strip()
                        with open(dest, 'wb') as g:
                                g.write(part.get_content())
                        #parser fichier

def filename_from_email_subject_and_email_id(**kwargs):
        #renvoyer l id et les 20 premiers caracteres du sujet
        #format_souhaite  = ('Date','Message-ID','Subject')
        format_souhaite  = ('Date','Subject')
        ##        return ''.join([ "{{contenu}:{fill}{align}{width}}}".
        ##                        format(contenu=kwargs['msg'].get(partie_msg),fill='_',
        ##                               align='^',width='10') for partie_msg in format_souhaite ])
        #return ''.join([ "{0:_^10}".format(contenu=kwargs['msg'].get(partie_msg)) for partie_msg in format_souhaite ])
        #return ''.join([ partie_msg for partie_msg in format_souhaite ])
        #return ''.join([ "{contenu:_^10}".format(contenu=kwargs['msg'].get(partie_msg)) for partie_msg in format_souhaite ])
        # resultat decevant: id pa utilisable; le vire
        #j ajoue un dico pour modifier facilement les camps avant renvoi resultat
        dico = { format_souhaite[i] : "{contenu:_^10}".format(contenu=kwargs['msg'].get(format_souhaite[i])) for i in range(len(format_souhaite)) }
        dico[format_souhaite[0]] = parse(dico[format_souhaite[0]])
        
        return repr(dico)
		
                

               

                        
                                
                

                                
def renommer(**kwargs):
        if 'nom_fichier' in kwargs and 'fonction_transfo_nom' in kwargs and 'msg' in kwargs :
                resultat =  kwargs['fonction_transfo_nom'](nom_fichier = kwargs['nom_fichier'], msg = kwargs['msg'])
                print(resultat)
                return resultat
        else:
                print("renommer : missing parameter")
        
        


#afficher()
#rechercher()
#parcourir(f=renommer,fonction_transfo_nom=filename_from_email_subject_and_email_id)
#for fichier in files:
fichier = 'noname (30).eml'
print(fichier)
m = Objet_mail(fichier)
print(m.getAttachmentCount())
for attachment in m.liste_pieces_jointes:
        print(attachment.mod_date, attachment.read_date,
              attachment.create_date, attachment.name,
              attachment.content_type, attachment.mailinstance.isfrom,
              attachment.mailinstance.issubject,
              attachment.getFileName(),
              attachment.getFileType(),
              #attachment.getFile(),
              attachment.mailinstance.getNormalizedName())
#piece_jointe()
        
                
                


        
                   
        

