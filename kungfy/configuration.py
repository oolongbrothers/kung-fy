"""
configuration
module for exposing configuration values
"""
import os


class Configuration(object):
    """
    A base configuration based on hard-coded default values
    """
    path_local_home = os.getenv("HOME")
    
    path_nas = '/media/nas'
    path_nas_config = path_nas + os.sep + 'Audio/.kung-fy'
    path_nas_lockfile = path_nas_config + os.sep + 'lock'
    path_nas_repository = 'rsync://nas.home::/kung-fy'
    path_nas_library = path_nas + os.sep + 'Audio/Musikbibliothek'

    path_local_config = path_local_home + os.sep + '.config/banshee-1'	
    path_local_config_backup = path_local_config + '.backup'

    path_local_kungfy = path_local_home + os.sep + '.kung-fy'
    path_local_library_link = path_local_kungfy + os.sep + '/library'
    path_local_library = path_local_home + os.sep + 'Audio/Musikbibliothek'

    path_player_bin = '/usr/bin/banshee'
    
    
    def __init__(self):
        if not os.path.exists(self.path_local_kungfy):
            os.mkdir(self.path_local_kungfy)
            print "created local settings folder %s" % self.path_local_kungfy
        else:
            if not os.path.isdir(self.path_local_kungfy):
                raise ValueError("Could not create local settings folder %s, name is taken by file." % self.path_local_kungfy)
                
                
