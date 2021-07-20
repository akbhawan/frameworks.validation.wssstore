"""
Standalone Execution builder class to build scenario json with all steps.
"""
import os
import csv
from standaloneapi.model.standalone_execution_model import StandaloneExecutionModel
from standaloneapi.executor.tws.tws_builder_abstract_scenario import BuilderAbstractScenario
from standaloneapi.executor.get_path import get_installation_path


class BuildStandaloneExecutionScenario(BuilderAbstractScenario):
    """
    Class initialize to Standalone Execution model and provide method to build model steps.
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
        path = os.path.join(get_installation_path(), "collateral", "standalone", "testdata.csv")
        with open(path, 'r') as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                if testcase in row['Testcase_ID'] or testcase in row['HSD_ID']:
                    return row
            else:
                raise Exception("Test case not found in the TC List - {}".format(testcase))

    def initialize_tws_scenario_model(self):
        """
        Initialize Standalone TWS Model
        """
        standalone_execution_model = StandaloneExecutionModel()
        return standalone_execution_model

    def build_tws_scenario_model(self, standalone_execution_model):
        """
        Build Standalone TWS Model
        standalone_model :arg
        """
        for testcase in self.testcase_list:
            testcase = str(testcase).strip()
            tc_info = self.read_testdata_from_csv(testcase)
            tc_name = testcase.replace("-", "_")
            func_name = "add_sub_scenario_{tc_name}".format(tc_name=tc_name)
            #print("mcp", getattr(standalone_execution_model, func_name))
            if hasattr(standalone_execution_model, func_name) and callable(getattr(standalone_execution_model, func_name)):
                self.scenario.add_step(getattr(standalone_execution_model, func_name)(testcase, tc_info))
            else:
                self.scenario.add_step(standalone_execution_model.add_sub_scenario_standalone_execution(testcase, tc_info))

    def return_tws_scenario_model(self):
        """
        Return Standalone scenario json model
        """
        return self.scenario
