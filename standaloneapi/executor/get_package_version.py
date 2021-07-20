import os
import requests
import json
from standaloneapi.executor.get_path import get_installation_path
from logger.logger_util import get_logger_instance
import configparser

CONFIG = configparser.ConfigParser()

LOG = get_logger_instance()

class PackageVersion:

    @staticmethod
    def get_package_version():
        """Function to find package version
        based on version file existence"""
        print("entered get package version")
        package_file_path = os.path.join(get_installation_path(), 'standaloneapi', 'package_version.txt')
        CONFIG.read(os.path.join(get_installation_path(), 'config.ini'))
        if (os.path.exists(package_file_path)):
            package_file = open(package_file_path, 'r')
            package_version = package_file.readline()

        else:
            dummy_package_version = 0
            get_url = requests.get("https://ubit-artifactory-or.intel.com/artifactory/"
                                   "api/storage/one-windows-pypi-local/wss_autoflow/develop")
            json_data = json.loads(get_url.text)
            json_list = json_data['children']
            CONFIG.read(os.path.join(os.getcwd(), 'config.ini'))
            for item in json_list:
                org_version = item['uri'][1:]
                version = int(item['uri'][1:].replace('.', ''))
                if version > dummy_package_version:
                    package_version = org_version
                    dummy_package_version = int(package_version.replace('.', ''))

        branch_name = CONFIG.get("BRANCHING", "branch_name")
        package_name = CONFIG.get("BRANCHING", "package_name")
        LOG.info("Installing Autoflow package version {}-{}".format(package_name, package_version))
        return package_version, branch_name, package_name

    @staticmethod
    def get_ifwi_package_version():
        """
        Function to find the ifwi api package version
        """
        CONFIG.read(os.path.join(get_installation_path(), 'config.ini'))
        dummy_package_version = 0
        get_url = requests.get("https://ubit-artifactory-or.intel.com/artifactory/"
                               "api/storage/one-windows-pypi-local/wss_autoflow/ifwi_api/")
        json_data = json.loads(get_url.text)
        json_list = json_data['children']
        CONFIG.read(os.path.join(os.getcwd(), 'config.ini'))
        for item in json_list:
            org_version = item['uri'][1:]
            version = int(item['uri'][1:].replace('.', ''))
            if version > dummy_package_version:
                package_version = org_version
                dummy_package_version = int(package_version.replace('.', ''))
        return package_version
