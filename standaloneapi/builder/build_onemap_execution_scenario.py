# Author: Anil Bhawangirkar

"""
OneMap Execution builder class to build scenario json with all steps.
"""
import os
import csv
from standaloneapi.model.onemap_execution_model import OneMapExecutionModel
from standaloneapi.executor.tws.tws_builder_abstract_scenario import BuilderAbstractScenario
from standaloneapi.executor.get_path import get_installation_path


class BuildOneMapExecutionScenario(BuilderAbstractScenario):
    """
    Class initialize to OneMap Execution model and provide method to build model steps.
    """
    def __init__(self, **kwargs):
        """
        Dictionary arguments:
        scenario: Dict<>
        framework: string
        """
        self.scenario = kwargs.get('scenario')
        self.testcase_list = kwargs.get("testcase_list")

    def read_testdata_from_csv(self, testcase):
        """
        Read OneMap TestData CSV
        """
        path = os.path.join(get_installation_path(), "collateral", "onemap", "testdata.csv")
        with open(path, 'r') as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                if testcase in row['Testcase_ID'] or testcase in row['HSD_ID']:
                    return row
            else:
                raise Exception("Test case not found in the TC List - {}".format(testcase))

    def initialize_tws_scenario_model(self):
        """
        Initialize OneMap TWS Model
        """
        onemap_execution_model = OneMapExecutionModel()
        return onemap_execution_model

    def build_tws_scenario_model(self, onemap_execution_model):
        """
        Build OneMap TWS Model
        standalone_model :arg
        """
        for testcase in self.testcase_list:
            tc_info = self.read_testdata_from_csv(testcase)
            self.scenario.add_step(onemap_execution_model.add_sub_scenario_onemap_execution(testcase, tc_info))

    def return_tws_scenario_model(self):
        """
        Return OneMap scenario json model
        """
        return self.scenario
