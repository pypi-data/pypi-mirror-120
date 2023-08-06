'''
Project Karen: Synthetic Human
Created on July 12, 2020
@author: lnxusr1
@license: MIT License
@summary: Core Library
'''

import os, sys
import logging 
import json 
import uuid
import shutil 

# version as tuple for simple comparisons 
VERSION = (0, 7, 1) 
# string created from tuple to avoid inconsistency 
__version__ = ".".join([str(x) for x in VERSION])
__app_name__ = "Project Karen"

# Imports for built-in features
#from .listener import Listener
#from .speaker import Speaker
try:
    from karen_device import DeviceContainer
except:
    pass 

try:
    from karen_brain import Brain
    from karen_brain.skillmanager import Skill, SkillManager
except:
    pass

def _getImport(libs, val):
    """
    Dynamically imports a library into memory for referencing during configuration file parsing.
    
    Args:
        libs (list):  The list of libraries already imported.
        val (str):  The name of the new library to import.
    
    Returns:
        (str): The name of the newly imported library.  If library is already imported then returns None.
    """

    if val is not None and isinstance(val,str) and val.strip() != "":
        if "." in val:
            parts = val.split(".")
            parts.pop()
            ret = ".".join(parts)
            if ret in libs:
                return None

            libs.append(ret)
            return ret

    return None

def start(configFile=None, log_level="info", log_file=None, overwriteConfig=True):
    """
    Static method to start a new instance of karen based on a provided configuration file.
    
    Args:
        configFile (str):  Path and Name of the JSON configuration file.
        log_level (str):  The level of logging to provide (critical, error, warning, info, and debug). (optional)
        log_file (str):  Path and Name of the log file to create (otherwise prints all messages to stderr). (optional)
        overwriteConfig (bool): Indicates if the ~/.karen/config.json should be overwritten with the supplied config.
    """
    
    localConfig = os.path.join(os.path.expanduser("~/.karen"),'config.json')

    if configFile is None:
        # If we have a file in "~/.karen/config.json" then use that one if none are specified
        if os.path.isfile(localConfig):
            configFile = localConfig 
            
    if configFile is None or str(configFile).lower() == "audio":
        configFile = os.path.abspath(os.path.join(os.path.dirname(__file__),"data","basic_config.json"))
    elif str(configFile).lower() == "video":
        configFile = os.path.abspath(os.path.join(os.path.dirname(__file__),"data","basic_config_video.json"))
    
    configFile = os.path.abspath(configFile)
    if not os.path.isfile(configFile):
        raise Exception("Configuration file does not exist.")
        quit(1)
    
    if overwriteConfig and configFile != localConfig:
        os.makedirs(os.path.dirname(localConfig), exist_ok=True)
        shutil.copyfile(configFile, localConfig) # Save for restart
    
    brain = None
    container = None 
        
    try:
        from karen_brain import start as kbrain_start
        brain = kbrain_start(configFile, log_level, log_file, x_wait=False)
    except ModuleNotFoundError:
        pass
    
    try:
        from karen_device import start as kdevice_start
        container = kdevice_start(configFile, log_level, log_file, x_wait=False)
    except ModuleNotFoundError:
        pass
    
    
    if container is not None:
        container.wait()
        
    if brain is not None:
        brain.wait()
        
    if brain._doRestart or container._doRestart:
        cmd = sys.executable + " " + " ".join(sys.argv)
        
        logger = logging.getLogger("RESTART")
        
        import time
        logger.info("Waiting for processes to close")
        time.sleep(5)
        logger.info("Restarting")
        
        myEnv = dict(os.environ)
        #myEnv["GREPDB"] = cmd
        #print(myEnv)
        
        #del myEnv["GIO_LAUNCHED_DESKTOP_FILE_PID"]
        #del myEnv["XDG_RUNTIME_DIR"]
        #del myEnv["GPG_AGENT_INFO"]
        
        #del myEnv["GDK_CORE_DEVICE_EVENTS"]
        #del myEnv["GIO_LAUNCHED_DESKTOP_FILE_PID"]
        #del myEnv["GIO_LAUNCHED_DESKTOP_FILE"]
        #del myEnv["IDE_PROJECT_ROOTS"]
        #del myEnv["LIBOVERLAY_SCROLLBAR"]
        #del myEnv["OXYGEN_DISABLE_INNER_SHADOWS_HACK"]
        #del myEnv["PYDEV_COMPLETER_PYTHONPATH"]
        #del myEnv["PYDEVD_SHOW_COMPILE_CYTHON_COMMAND_LINE"]
        #del myEnv["PYTHONIOENCODING"]
        #del myEnv["PYTHONPATH"]
        #del myEnv["PYTHONUNBUFFERED"]
        #del myEnv["QT_QPA_FONTDIR"]
        
        if "QT_QPA_PLATFORM_PLUGIN_PATH" in myEnv:
            del myEnv["QT_QPA_PLATFORM_PLUGIN_PATH"]    
        
        #myEnv = {"QT_DEBUG_PLUGINS": "offscreen", "DISPLAY": str(os.environ["DISPLAY"]), 'GREPDB': cmd }
        
        import subprocess
        subprocess.Popen(cmd, shell=True, stdout=sys.stdout, stderr=sys.stderr, stdin=sys.stdin,
            env=myEnv)
