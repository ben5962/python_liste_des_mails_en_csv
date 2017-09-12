#!/usr/bin/env python
"""
pipreqs.py: run ``pip install`` iteratively over a requirements file.


Usage:
    requirements.py <nom_reqfile>

Options:
    -o, --options-pip <options_pip> [default: None]
"""

import sys
from docopt import docopt
RETCODE_SUCCES = 0
RETCODE_ECHEC = 1
def main(args):
    print(args)
    if '<nom_reqfile>' in args:
        filename = args['<nom_reqfile>']
    
    
        import pip
        retcode = 0
        with open(filename, 'r') as f:
            for line in f:
                pipcode = pip.main(['install', line.strip()])
                retcode = retcode or pipcode
            return RETCODE_SUCCES
    else:
        return RETCODE_ECHEC
if __name__ == '__main__':
    import sys
    #sys.exit(main(sys.argv[1:]))
    print(sys.argv)
    arguments = docopt(__doc__)
    print(arguments)
    sys.exit(main(arguments))
