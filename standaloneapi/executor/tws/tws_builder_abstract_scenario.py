"""
File: builder_abstract_scenario
Description: Abstract class to  Build TWS Scenario
"""
from abc import ABC, abstractmethod


class BuilderAbstractScenario(ABC):
    """ Abstract class - BuilderAbstractScenario"""

    @abstractmethod
    def initialize_tws_scenario_model(self):
        """
        Initialize TWS Scenario Model
        :return:
        """
        raise NotImplementedError("Subclasses should implement initialize_tws_scenario_model!")

    @abstractmethod
    def build_tws_scenario_model(self, ifwi_model):
        """
        Build TWS Scenario TWS Model
        :return:
        """
        raise NotImplementedError("Subclasses should implement build_tws_scenario_model!")

    @abstractmethod
    def return_tws_scenario_model(self):
        """
        Return TWS Scenario Model
        :return:
        """
        raise NotImplementedError("Subclasses should implement return_tws_scenario_model!")
