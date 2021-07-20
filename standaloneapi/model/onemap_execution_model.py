# Author: Anil Bhawangirkar

"""
File: onemap_execution_model.py
Model to implement Test Execution Scenario
"""
from standaloneapi.executor.tws.generate.scenario_generator import ScenarioGenerator
from standaloneapi.executor.tws.generate.step_generator import StepGenerator


class OneMapExecutionModel:
    """
    Execution model
    """
    def __init__(self, **kwargs):
        """
        Initialize model arguments
        :param kwargs:
        """
        pass

    @staticmethod
    def install_python_package():
        """
        Install Python Package
        :return: tws_Step
        """
        variables = {
            "src_code": "%af-src-path%\\source\\provision\\collection\\resources",
        }
        step = StepGenerator(name="Install Python Package")
        step.setVariables(variables)
        step.setParameters("-executionpolicy bypass -File %src_code%\\python_installation.ps1")
        step.setExecutable("powershell.exe")
        return step.generate_tws_step_json()

    @staticmethod
    def install_wit_tool():
        """
        Install WIT Tool
        :return: tws_Step
        """
        step = StepGenerator(name="Install WIT Tool")
        step.setParameters(
            "C:\ProgramData\chocolatey\choco.exe install wit"
            " -source=https://ubit-artifactory.intel.com/artifactory/api/nuget/occ-nuget --version=6.1.49 /Y")
        step.setExecutable("powershell.exe")
        return step.generate_tws_step_json()

    @staticmethod
    def install_choco_tool():
        """
        Install Choco Tool
        :return: tws_Step
        """
        step = StepGenerator(name="Install Choco Tool")
        step.setParameters('''Get-Command chocolatey
            if ($? -eq $false) {
                #install chocolatey
                Set-ExecutionPolicy Bypass -Scope Process 
                -Force; [System.Net.ServicePointManager]::SecurityProtocol = 
                [System.Net.ServicePointManager]::SecurityProtocol -bor 3072;
                 iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
            }''')
        step.setExecutable("powershell.exe")
        return step.generate_tws_step_json()

    @staticmethod
    def run_onemap_test_execution_script(testcase, tc_info):
        """
        Run OneMap Test Execution Scripts
        :return: tws_Step
        """
        tc_name = str(testcase).strip()
        if tc_info:
            tc_title = f"Execute Step {tc_info['Testcase_Name']}"
        else:
            tc_title = tc_name
        step = StepGenerator(name="{tc_name}".format(tc_name=tc_title), timeout=50000)
        script_path = "C:\\Users\\intel\\Desktop\\Testcases\\QAC\\{tc_name}\\{tc_name}.py".format(tc_name=tc_name)
        step.setParameters(script_path)
        step.setRequiresDict('HOST')
        return step.generate_tws_step_json()

    def add_sub_scenario_onemap_execution(self, testcase, tc_info):
        """
        Sub-scenario step for OneMap Execution.
        :return:
        """
        tc_name = str(testcase).strip()
        tc_title = f"{tc_name} - {str(tc_info['Domain']).lower()} - {str(tc_info['Testcase_Name']).lower()}"
        sub_sc = ScenarioGenerator(name=tc_title)
        sub_sc.add_step(self.run_onemap_test_execution_script(testcase, tc_info))
        return sub_sc.generate_scenario()
