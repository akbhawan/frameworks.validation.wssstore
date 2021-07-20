"""
File: prepare_tws_scenario
Description: Abstract class to  Prepare TWS Scenario
"""
from abc import ABC, abstractmethod


class TwsPrepareScenario(ABC):
    """ Abstract class - PrepareTwsScenario"""

    @abstractmethod
    def generate_scenario_json(self):
        """
        Generates scenario JSON
        :return:
        """
        raise NotImplementedError("Subclasses should implement generate_tws_json!")

    @abstractmethod
    def prepare_scenario_json(self):
        """
        Prepare scenario JSON
        :return:
        """
        raise NotImplementedError("Subclasses should implement prepare_scenario_json!")
