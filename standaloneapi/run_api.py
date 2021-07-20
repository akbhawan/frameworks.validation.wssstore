# Author: Anil Bhawangirkar

"""
This will be a facade for AutoFlow 2.0 componets fetch provision and run
Any external world access will go through this class.
All the Click commands and REST API calls will initiate AutoFlow class
and access the respective methods.
All the error handling and returning status will be handled here

"""
from logger.logger_util import get_logger_instance
from standaloneapi.run_prepare_scenario import PrepareTestScenario
LOG = get_logger_instance()


class RunScenarioAPI:
    """
    AutoFlow Base Class for all the external interfaces(cli/flask).
    This class provides all the methods of AutoFlow functionalities (Fecth/Provision/Execution).
    """

    def __init__(self, **kwargs):

        self.phase = kwargs.get('phase')
        self.location = kwargs.get('location')
        self.platform = kwargs.get('platform')
        self.framework_version = kwargs.get('framework_version')
        self.framework = kwargs.get('framework')
        self.execution_type = kwargs.get('execution_type')
        self.testcases = kwargs.get('testcases')
        self.timeout = kwargs.get('timeout')
        self.splunk_metadata = kwargs.get('splunk_metadata')

    def generate_standalone_scenario(self):
        """
        Generate JSON and Run the RAILS TestCase Execution
        for (Bronze/Silver) using TWS Post-Scenario and returns results.
        :return: Execution Results Status
        """

        testcase_list = str(self.testcases).split(',')
        try:
            run_test_executioner = PrepareTestScenario(
                testcase_list=testcase_list,
                timeout=self.timeout,
                framework=self.framework,
                splunk_metadata=self.splunk_metadata
            )
            # if sut_list.count > 1 :Fanout option
            scenario_json = run_test_executioner.generate_scenario_json()
            LOG.info("Scenario Json Created Successfully {}".format(scenario_json))
            return scenario_json
        except Exception as error:
            LOG.error(
                "Run Test failed with exception: {}".format(error))
            return {
                'status': 'Failure',
                'message': 'Error while executing run tests :' + error.__str__()
            }

    def generate_onemap_scenario(self):
        """
        Generate JSON and Run the RAILS TestCase Execution
        for (Bronze/Silver) using TWS Post-Scenario and returns results.
        :return: Execution Results Status
        """

        testcase_list = str(self.testcases).split(',')
        try:
            run_test_executioner = PrepareTestScenario(
                testcase_list=testcase_list,
                timeout=self.timeout,
                framework=self.framework,
                splunk_metadata=self.splunk_metadata
            )
            # if sut_list.count > 1 :Fanout option
            scenario_json = run_test_executioner.generate_scenario_json()
            LOG.info("Scenario Json Created Successfully {}".format(scenario_json))
            return scenario_json
        except Exception as error:
            LOG.error(
                "Run Test failed with exception: {}".format(error))
            return {
                'status': 'Failure',
                'message': 'Error while executing run tests :' + error.__str__()
            }
