'''
Created on Jan 12, 2011

@author: alex
'''

import os
import subprocess
import shutil
import time


lockfile_fail_message = '''
Lock file exists.
This probably means that another client has checked out the configuration currently. To resolve this, close the other client and try again.
If the problem persists or no other client is running on the same config repository, an unclean shutdown has probably occurred. Please review the situation manually and remove the lock file manually from the config repository after you have fixed the repository.
'''


class Engine(object):
    
    def run_sequence(self):
        self.prepare()
        self.run_player()
        self.wrap_up()
    
    def prepare(self):
        pass
    
    def run_player(self):
        pass
    
    def wrap_up(self):
        pass


class TestEngine(Engine):
    
    def __init__(self, configuration):
        self.configuration = configuration
    
    def prepare(self):
        print("Preparing configuration...")
        yield True, "Loading Stuffs Up"
        time.sleep(1)
        message = "Could not find or mount the configuration folder: " + self.configuration.path_nas_config
        yield True, message
        return
        time.sleep(1)
        yield True, "Modifying Brains"
        time.sleep(1)
    
    def run_player(self):
        print("Running player...")
        time.sleep(2)
        yield False, "Done"
    
    def wrap_up(self):
        print("Persisting changes...")
        yield True, "Putting Stuffs in Shelves"
        time.sleep(1)
        yield True, "Telling Mom On You"
        time.sleep(1)
        yield True, "Something Went Wrong"


class RemoteEngine(Engine):
    
    def __init__(self, configuration):
        self.configuration = configuration

    def prepare(self):
        if not os.path.exists(self.configuration.path_nas_config):
            message = "Trying to mount nas"
            print(message)
            yield True, message
            # connect via OpenVPN ?
            if not self._mount_nas():
                message = "Could not find or mount the configuration folder: " + self.configuration.path_nas_config
                print message
                yield False, message
                return
            
        if os.path.exists(self.configuration.path_nas_lockfile):
            print(lockfile_fail_message)
            yield False, lockfile_fail_message
            return 
            
        message = "Creating lock file"
        print(message + " : " + self.configuration.path_nas_lockfile)
        yield True, message
        try:
            open(self.configuration.path_nas_lockfile, 'w').close()
        except:
            message = "Failed to create lock file"
            print message
            yield False, message
            return
            
        message = "Backing up local configuration"
        print(message)
        yield True, message
        try:
            if os.path.exists(self.configuration.path_local_config):
                if os.path.exists(self.configuration.path_local_config_backup):
                    shutil.rmtree(self.configuration.path_local_config_backup)
                shutil.move(self.configuration.path_local_config, self.configuration.path_local_config_backup)
        except:
            message = "Error backing up remote config folder: " + self.configuration.path_local_config
            print(message)
            yield False, message
            return

        message = "Downloading configuration from nas"
        print(message + ": " + self.configuration.path_nas_repository)
        yield True, message
        try:
            self._download_config(self.configuration.path_nas_repository, self.configuration.path_local_config)
        except:
            message = "Error downloading remote configuration"
            print(message)
            yield False, message
            # clean up
            shutil.rmtree(self.configuration.path_local_config, True)
            if os.path.exists(self.configuration.path_local_config_backup):
                shutil.move(self.configuration.path_local_config_backup, self.configuration.path_local_config)
            return
        
        message = "Pointing library to nas"
        print(message + ": " + self.configuration.path_nas_library)
        yield True, message
        self._reset_symlink(self.configuration.path_local_library_link, self.configuration.path_nas_library)
        
    def run_player(self):
        message = "Executing player binary"
        print(message + ": " + self.configuration.path_player_bin)
        yield True, message
        process = subprocess.Popen(self.configuration.path_player_bin, shell=False, stdout=subprocess.PIPE)
        process.wait()
        print("banshee return code: " + str(process.returncode))
        
    def wrap_up(self):
        message = "Pointing library to local"
        print(message + ": " + self.configuration.path_local_library)
        yield True, message
        self._reset_symlink(self.configuration.path_local_library_link, self.configuration.path_local_library)
        
        message = "Copying configuration to nas"
        print(message + ": " + self.configuration.path_nas_repository)
        yield True, message
        
        try:
            self._upload_config(self.configuration.path_local_config, self.configuration.path_nas_repository)
        except:
            message = "Error uploading configuration"
            yield False, message
            return
        
        message = "Wrapping up"
        print(message)
        yield True, message
        try:            
            print("Removing lock file: " + self.configuration.path_nas_lockfile)
            os.remove(self.configuration.path_nas_lockfile)
            print("Removing backup configuration: " + self.configuration.path_local_config_backup)    
            shutil.rmtree(self.configuration.path_local_config_backup)
        except:
            message = "Error wrapping up"
            print message
            yield False, message
            return
        
    def _mount_nas(self):
        success = False
        process = subprocess.Popen('mount ' + self.configuration.path_nas, shell=True)
        returncode = process.wait()
        # debug
        print("mount return code: " + str(process.returncode))
        time.sleep(3)
        if not returncode and os.path.exists(self.configuration.path_nas_config):
            success = True
        return success
    
    def _download_config(self, path_remote, path_local):
        process = subprocess.Popen('duplicity restore --no-encryption ' + path_remote + '/ ' + path_local, shell=True)
        returncode = process.wait()
        # debug
        print("duplicity return code: " + str(process.returncode))
        if returncode:
            raise IOError()
    
    def _upload_config(self, path_local, path_remote):
        process = subprocess.Popen('duplicity --no-encryption --allow-source-mismatch --full-if-older-than 1M ' + path_local + ' ' + path_remote + '/', shell=True)
        returncode = process.wait()
        # debug
        print("duplicity return code: " + str(process.returncode))
        if returncode:
            raise IOError()
        
    def _reset_symlink(self, symlink, target):
        if os.path.exists(symlink):
            os.remove(symlink)
        os.symlink(target, symlink)

