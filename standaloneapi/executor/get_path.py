from distutils.sysconfig import get_python_lib
import os
import configparser


def get_installation_path():
    currentWorkingDir = os.getcwd()
    dirs = os.listdir(currentWorkingDir)
    if "config.ini" in dirs:
        config = configparser.ConfigParser()
        config.read(os.path.join(os.getcwd(), 'config.ini'))
        lib_path = config.get("LIB_PATH", "af_package_path")
        if lib_path == "true":
            return currentWorkingDir
    return get_python_lib()
