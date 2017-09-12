invalid_chars_in_filename='<>:"/\\|?*\%\''+''.join([chr(x) for x in range(32)])
reserved_filenames = ["CON", "PRN", "AUX", "NUL",
"COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9"
"LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"]


def clean_windows_filename_string(filename):
    trantab = str.maketrans(invalid_chars_in_filename, '_'*len(invalid_chars_in_filename))
    return filename.translate(trantab)

def getAvailibleFileName(filename,iterable,nbmaxdoublons=3):
    cpt = 0
    candidat = filename
    while candidat in iterable and cpt <= nbmaxdoublons:
        print('getAvailibleFilename : candidat {} trouve dans la liste: '.format(candidat))
        #formation nv candidat
        cpt = cpt + 1
        alt_decompte_doublon = "{i:{fill}{width}}".format(i=cpt,fill=0,width=3)
        candidat = 'doublon-' + alt_decompte_doublon + filename
        print('getAvailibleFilename : formation d un nouveau candidat candidat {}: '.format(candidat))
        
        
    if cpt == nbmaxdoublons:
        raise ValueError("nbmaxdoublons atteint: {}".format(nbmaxdoublons))
    print('getAvailibleFilename : candidat candidat accepte {}: '.format(candidat))
    return candidat
        
        
        

def copy_to(filein, filecopyname,destdir):
    #verifier que filecopyname n existe pas deja
    from pathlib import Path
    curdir = Path('.')
    fich_in = curdir / filein
    if not fich_in.is_file():
        raise ValueError("fich_in doit exister pour etre copie {}".format(fich_in))

    #verifier que le rep de dest exite bien
    repdest = Path('.') / destdir
    if not repdest in [x for x in curdir.iterdir() if x.is_dir()]:
        raise ValueError("repdest doit exister pour etre destination {}".format(repdest))

    # s il existe deja
    # compteur = 01
    # tant que filecopyname existe deja
    # appeler filecopyname "doublon<01-99>filecopyname"
    # ajouter 1 a compteur
    chemin = Path('.') / destdir
    candidat_choisi = getAvailibleFileName(filecopyname, [chemin_complet_fichier.name for chemin_complet_fichier in chemin.iterdir()])
    fich_out = chemin / candidat_choisi
    import shutil
    shutil.copyfile(fich_in,fich_out)
            
    

    
    #creer fichier temporaire .temp
    
    #copier filein vers .temp
    # renommer .temp en filecopyname
