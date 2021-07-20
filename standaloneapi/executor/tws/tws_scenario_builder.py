"""
File: prepare_tws_scenario
Description: Abstract class to  Prepare TWS Scenario
"""
from abc import ABC, abstractmethod


class TwsScenarioBuilder(ABC):
    """ Abstract class - TwsScenarioModel"""

    @abstractmethod
    def initialize_tws_scenario(self):
        """
        Initialize TWS Scenario
        :return:
        """
        raise NotImplementedError("Subclasses should implement initialize_tws_scenario!")

    @abstractmethod
    def build_tws_scenario(self):
        """
        Build TWS Scenario
        :return:
        """
        raise NotImplementedError("Subclasses should implement build_tws_scenario!")

    @abstractmethod
    def generate_tws_scenario(self):
        """
        Generates tws scenario JSON
        :return:
        """
        raise NotImplementedError("Subclasses should implement generate_tws_json!")

