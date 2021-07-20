"""
Execution build factory to choose different execution builder.
"""
from standaloneapi.builder.build_standalone_execution_scenario import BuildStandaloneExecutionScenario
from standaloneapi.builder.build_onemap_execution_scenario import BuildOneMapExecutionScenario


class ExecutionBuilderFactory:
    """
    Class to initialize builder factory and provide methods to choose builder.
    """
    def __init__(self, **kwargs):
        """
        Dictionary arguments:
        scenario: Dict<>
        framework: string
        post_provision_script: string
        """
        self.scenario = kwargs.get('scenario')
        self.testcase_list = kwargs.get("testcase_list")
        self.framework = kwargs.get('framework')
        self.execution_type = kwargs.get('execution_type')
        self.execution_time = kwargs.get('execution_time')
        self.splunk_metadata = kwargs.get('splunk_metadata')
        self.install_dependency = kwargs.get('install_dependency')

    def get_builder_instance(self):
        """
        Method to choose builder based on flashing type
        return: builder_instance
        """
        if self.framework == 'standalone':
            builder_instance = BuildStandaloneExecutionScenario(
                scenario=self.scenario,
                testcase_list=self.testcase_list,
                splunk_metadata=self.splunk_metadata
            )
        else:
            builder_instance = BuildOneMapExecutionScenario(
                scenario=self.scenario,
                testcase_list=self.testcase_list,
                splunk_metadata=self.splunk_metadata
            )
        return builder_instance
