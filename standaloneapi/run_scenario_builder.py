# Author: Anil Bhawangirkar

"""
Module to implement Execution Scenario Json.
"""
from logger.logger_util import get_logger_instance
from standaloneapi.executor.get_package_version import PackageVersion
from standaloneapi.executor.tws.generate.scenario_generator import ScenarioGenerator
from standaloneapi.executor.tws.tws_scenario_builder import TwsScenarioBuilder
from standaloneapi.run_builder_factory import ExecutionBuilderFactory

LOG = get_logger_instance()
package = PackageVersion()


class ExecutionScenarioBuilder(TwsScenarioBuilder):
    """
    Model to Generate Scenario JSON for Execution Scenario
    """
    def __init__(self, **kwargs):
        """
        Initialise arguments
        :param kwargs:
        """
        self.testcase_list = kwargs.get("testcase_list")
        self.scenario = ScenarioGenerator(
            name=f"{kwargs.get('name')}",
            sut=kwargs.get('sut'),
            host=kwargs.get('host')
        )
        self.sc_path = kwargs.get('scenario_path')
        self.package_version = ""
        self.controller = kwargs.get("controller")
        self.framework = kwargs.get('framework')
        self.sut = kwargs.get("sut")
        self.host = kwargs.get("host")
        self.package_name = ""
        self.branch_name = ""
        self.splunk_metadata = kwargs.get('splunk_metadata')
        self.execution_type = kwargs.get('execution_type')
        self.execution_time = kwargs.get('execution_time')
        self.install_dependency = kwargs.get('install_dependency')


    def initialize_tws_scenario(self):
        """Initialize the TWS Scenario Class"""
        LOG.info("Initializing TWS Scenario")
        #self.package_version, self.branch_name, self.package_name = package.get_package_version()
        LOG.info("Package Version = {package_version}".format(package_version=self.package_version))
        variables = {
            "local-path": "C:\\TestSuite\\",
            "python-path": "py",
            "package_version": self.package_version,
            "package_name": self.package_name,
            "branch_name": self.branch_name,
            "af-src-path": "C:\\TestSuite\\{package_name}-{version}".format(
                package_name=self.package_name, version=self.package_version)
        }
        self.scenario.setVariables(variables)
        self.scenario.setRequiresController()
        if self.framework == 'onemap':
            self.scenario.setRequiresHost()
        else:
            self.scenario.setRequiresSut()

    def build_tws_scenario(self):
        """Build the TWS Scenario"""
        LOG.info("Building TWS Scenario")
        execution_builder_factory = ExecutionBuilderFactory(
            scenario=self.scenario,
            framework=self.framework,
            testcase_list=self.testcase_list,
            execution_type=self.execution_type,
            execution_time=self.execution_time,
            splunk_metadata=self.splunk_metadata,
            install_dependency=self.install_dependency
        )
        builder_instance = execution_builder_factory.get_builder_instance()
        execution_model = builder_instance.initialize_tws_scenario_model()
        builder_instance.build_tws_scenario_model(execution_model)
        self.scenario = builder_instance.return_tws_scenario_model()

    def generate_tws_scenario(self):
        """Generate TWS Json to the specified path"""
        LOG.info("Generate TWS Scenario.")
        sc_dict = self.scenario.generate_scenario()
        sc_json = self.scenario.convert_dict_to_json(sc_dict)
        self.scenario.write_scenario_to_file(sc_json, self.sc_path)
        return sc_json
