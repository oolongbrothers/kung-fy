# -*- coding: utf-8 -*-
'''
kung-fy - Script for nas-based banshee configuration storage

Created on Dec 9, 2010

@author: alex
'''

import sys
import getopt
import gui
import gtk
from engine import RemoteEngine
from configuration import Configuration 

__version__ = '0.5.0'

title_message = '''kung-fy v%s - Script for nas-based banshee state storage\n''' % __version__
usage_message = '''    Specify flag -n or --nogui to run as command-line utility without gui.
'''

def usage():
    print(usage_message)
    

def main(argv):
    print(title_message)
    nogui = False
    try:                                
        opts, args = getopt.getopt(argv, "hn", ["help", "nogui"]) #@UnusedVariable
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts: #@UnusedVariable
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ('-n', '--nogui'):
            nogui = True
    
    configuration = Configuration()
    if nogui:
        RemoteEngine(configuration).run_sequence()
    else:
        gui.Gui(RemoteEngine(configuration))
        gtk.main()


if __name__ == "__main__":
    main(sys.argv[1:])
