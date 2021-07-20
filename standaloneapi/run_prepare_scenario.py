# Author: Anil Bhawangirkar

"""
Module to prepare Test Execution Scenario JSON object and generate json file based on provision path.
"""
import errno
import os
import shutil

from standaloneapi.executor.get_path import get_installation_path
from standaloneapi.executor.tws.tws_prepare_scenario import TwsPrepareScenario
from standaloneapi.run_scenario_builder import ExecutionScenarioBuilder

from logger.logger_util import get_logger_instance
LOG = get_logger_instance()


class PrepareTestScenario(TwsPrepareScenario):
    """
    Class to generate hostprep scenario json.
    """

    def __init__(self, **kwargs):
        self.controller = kwargs.get("controller")
        self.sut = kwargs.get("sut")
        self.host = kwargs.get("host")
        self.framework = kwargs.get("framework")
        self.testcase_list = kwargs.get("testcase_list")
        self.json_req = kwargs.get('json_req')
        self.splunk_metadata = kwargs.get('splunk_metadata')
        self.execution_type = kwargs.get('execution_type')
        self.execution_time = kwargs.get('execution_time')
        self.install_dependency = kwargs.get('install_dependency')
        self.json_obj = None

    def generate_scenario_json(self):
        """Generate Test Execution TWS JSON for AF/NS."""
        LOG.info("Generating scenario JSON")
        scenario_json = self.prepare_scenario_json()

        if not os.path.exists(scenario_json):
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), scenario_json)
        LOG.info(f"Scenario Json {scenario_json}")
        if self.json_req:
            return self.json_obj
        else:
            return scenario_json

    def prepare_scenario_json(self):
        """
        Generate the relevant based scenario json in run scenario folder
        :return: Test Execution scenario json path
        """
        LOG.info("Preparing Scenario Json")
        scenario_path = None
        # if self.flash_type is not None:
        scenario_path = os.path.join(
            get_installation_path(),
            "source",
            "run",
            "scenario",
            "Automation_{}_TestSuite.json".format(self.framework.upper()))
        execution_builder = ExecutionScenarioBuilder(
            name="Automation {} TestSuite".format(self.framework.upper()),
            scenario_path=scenario_path,
            testcase_list=self.testcase_list,
            controller=self.controller,
            sut=self.sut,
            host=self.host,
            framework=self.framework,
            execution_type=self.execution_type,
            execution_time=self.execution_time,
            install_dependency=self.install_dependency,
            splunk_metadata=self.splunk_metadata
        )
        LOG.info(f"Scenario json path = {scenario_path}".format(scenario_path=scenario_path))
        execution_builder.initialize_tws_scenario()
        execution_builder.build_tws_scenario()
        self.json_obj = execution_builder.generate_tws_scenario()
        output_json_path = os.path.join(os.getcwd(),
                                        'AF_Output', 'execution')
        self.create_directory(output_json_path)
        shutil.copy(scenario_path, output_json_path)
        execution_json_path = os.path.join(output_json_path, os.path.basename(scenario_path))
        LOG.debug(f'Test Execution Scenario JSON in Output path : {execution_json_path}')
        return scenario_path

    def create_directory(self, folder_path):
        """Checks if the directory exists and creates if not"""
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)
