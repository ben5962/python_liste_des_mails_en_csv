# coding: utf8

'''
Created on 2 juil. 2017

@author: Utilisateur
'''

class Parcours(object):
    '''
    classdocs parcourt un r�pertoire et...
    - soit effectue une action pass�e en param�tre
    - soit affiche le contenu de chaque fichier
    
    - filtrage par fin de fichier
    - possibilit� de ne sortir que le premier fichier
    - possibilit� de ne sortir que le n-ieme
    - possibilit� de compter les fichiers.
    '''


    def __init__(self, glob=None, root=None, type_parcours=None):
        '''
        Constructor
        '''
        
        self.setGlob(glob) if glob is not None else self.setGlob("")
        self.setRoot(root) if root is not None else self.setRoot("")
        self.setParcours(type_parcours) if type_parcours is not None else self.setParcours("")
    
    def getTypesPossiblesParcours(self):
        parcours = ["repertoire"]
        def getFirst():
            return parcours[0]
        def getAll():
            return parcours
    
    def setParcours(self, parcours):
        if parcours in self.getTypesPossiblesParcours().getAll():
            self.parcours = parcours
        else:
            self.parcours = self.getTypesPossiblesParcours().getFirst()
        
    def setGlob(self,glob):
        self.glob = glob
    
    def setRoot(self, root):
        self.root = root
        
    def getFirstFilePath(self):
        pass
        
    
    