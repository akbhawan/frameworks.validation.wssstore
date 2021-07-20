"""
File: standalone_execution_model.py
Model to implement Test Execution Scenario
"""
from standaloneapi.executor.tws.generate.scenario_generator import ScenarioGenerator
from standaloneapi.executor.tws.generate.step_generator import StepGenerator


class StandaloneExecutionModel:
    """
    Execution model
    """
    def __init__(self, **kwargs):
        """
        Initialize model arguments
        :param kwargs:
        """
        self.execution_script = None
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

    def download_test_execution_script(self):
        """
        Download the Test Execution Scripts
        :return: tws_Step
        """
        tc_name = str(self.execution_script).strip().partition("PSPV-")[2]
        tc_id = "PSPV-" + tc_name.split()[0]
        step = StepGenerator(name="Download the Test Execution Scripts - {}".format(tc_id))
        target_path = "C:\\TestSuite"
        step.setParameters(
            "wit fetch --Artifactory-Full-Url "
            "https://ubit-artifactory.intel.com/artifactory/one-windows-pypi-repos/wss_autoflow/tools/2.0/packages/{}.zip "
            "--RemoveExtractedContent --Path {}".format(tc_id, target_path))
        step.setExecutable("powershell.exe")
        return step.generate_tws_step_json()

    @staticmethod
    def run_standalone_execution_script(testcase, tc_info):
        """
        Run the Test Execution Scripts
        :return: tws_Step
        """
        tc_name = str(testcase).strip()
        tc_title = f"Execute Step {tc_info['Testcase_Name']}"
        timeout = int(tc_info['Timeout_in_Mins']) * 60
        step = StepGenerator(name="{tc_name}".format(tc_name=tc_title), timeout=timeout)
        script_path = "C:\\FrameWork\\testcase\\{tc_name}\\{tc_name}.py".format(tc_name=tc_name)
        step.setParameters(script_path)
        return step.generate_tws_step_json()

    @staticmethod
    def run_standalone_sub_execution_script(testcase, tc_info, script_no):
        """
        Run the Test Execution Scripts
        :return: tws_Step
        """
        tc_name = str(testcase).strip()
        tc_title = f"Execute Step {tc_info['Testcase_Name']} - {script_no}"
        timeout = int(tc_info['Timeout_in_Mins']) * 60
        step = StepGenerator(name="{tc_name}".format(tc_name=tc_title), timeout=timeout)
        if script_no == 0:
            script_path = "C:\\FrameWork\\testcase\\{tc_name}\\{tc_name}.py".format(tc_name=tc_name)
        else:
            script_path = "C:\\FrameWork\\testcase\\{tc_name}\\{tc_name}_{script_no}.py".format(
                tc_name=tc_name, script_no=script_no)
        step.setParameters(script_path)
        step.setCritical(True)
        return step.generate_tws_step_json()

    def add_sub_scenario_repeat_execution(self, testcase, tc_info, script_no, repetitions):
        tc_name = testcase
        tc_title = f"{tc_name} - {str(tc_info['Domain']).lower()} - {str(tc_info['Testcase_Name']).lower()}"
        sub_sc = ScenarioGenerator(name=tc_title)
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, script_no))
        sub_sc.add_step(self.wait_toolcase_service_down())
        sub_sc.add_step(self.wait_toolcase_service_up())
        sub_sc.setRepetation(repetitions)
        return sub_sc.generate_scenario()

    @staticmethod
    def restart_system():
        """
        Restart system
        :return: tws_step
        """
        step = StepGenerator(name="Restart system", timeout=600)
        step.setType("tws_reboot")
        return step.generate_tws_step_json()

    @staticmethod
    def wait_toolcase_service_down():
        """
-        Wait for remote TCS service to go down
        :return: tws_Step
        """
        step = StepGenerator(name="Wait for remote TCS service to go down", timeout=600)
        step.setParameters(
            "-m ubit.scripts.monitor_service --meta localhost:7072 "
            "--max 600 down service_id:%SUT.service_id% --include-reserved")
        step.setRequiresDict("Controller")
        step.setCwd("%Controller.cwd%")
        step.setExecutable("%Controller.host:python%")
        step.setWaitBeforeExecutionTime(45)
        return step.generate_tws_step_json()

    @staticmethod
    def wait_toolcase_service_up():
        """
        Wait for monitor service to start
        :return: tws_Step
        """
        step = StepGenerator(name="Wait for monitor service to start", timeout=800)
        step.setParameters(
            "-m ubit.scripts.monitor_service --meta localhost:7072"
            " --max 4510 up service_id:%SUT.service_id% --include-reserved")
        step.setRequiresDict("Controller")
        step.setCwd("%Controller.cwd%")
        step.setExecutable("%Controller.host:python%")
        return step.generate_tws_step_json()

    def add_sub_scenario_standalone_execution(self, testcase, tc_info):
        """
        Sub-scenario step for Standalone Execution.
        :return:
        """
        tc_name = testcase
        num_script = int(tc_info['Test_Scripts_Count'])
        tc_title = f"{tc_name} - {str(tc_info['Domain']).lower()} - {str(tc_info['Testcase_Name']).lower()}"
        sub_sc = ScenarioGenerator(name=tc_title)
        if tc_info['Dependencies'] == 'Shutdown' or tc_info['Dependencies'] == 'Restart' \
                or tc_info['Dependencies'] == 'G3' or tc_info['Dependencies'] == 'S3'\
                or tc_info['Dependencies'] == 'S4' or tc_info['Dependencies'] == 'S4 and Restart':
            if num_script > 1:
                for i in range(0, num_script):
                    if i == num_script-1:
                        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, i))
                    else:
                        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, i))
                        sub_sc.add_step(self.wait_toolcase_service_down())
                        sub_sc.add_step(self.wait_toolcase_service_up())
        else:
            sub_sc.add_step(self.run_standalone_execution_script(testcase, tc_info))
        return sub_sc.generate_scenario()

    def add_sub_scenario_PSPV_TC_14094(self, testcase, tc_info):
        tc_name = testcase
        tc_title = f"{tc_name} - {str(tc_info['Domain']).lower()} - {str(tc_info['Testcase_Name']).lower()}"
        sub_sc = ScenarioGenerator(name=tc_title)
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 0))
        sub_sc.add_step(self.wait_toolcase_service_down())
        sub_sc.add_step(self.wait_toolcase_service_up())
        sub_sc.add_step(self.add_sub_scenario_repeat_execution(testcase, tc_info, 1, 5))
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 2))
        return sub_sc.generate_scenario()

    def add_sub_scenario_PSPV_TC_14054(self, testcase, tc_info):
        tc_name = testcase
        tc_title = f"{tc_name} - {str(tc_info['Domain']).lower()} - {str(tc_info['Testcase_Name']).lower()}"
        sub_sc = ScenarioGenerator(name=tc_title)
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 0))
        sub_sc.add_step(self.wait_toolcase_service_down())
        sub_sc.add_step(self.wait_toolcase_service_up())
        sub_sc.add_step(self.add_sub_scenario_repeat_execution(testcase, tc_info, 1, 5))
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 2))
        return sub_sc.generate_scenario()

    def add_sub_scenario_PSPV_TC_14055(self, testcase, tc_info):
        tc_name = testcase
        tc_title = f"{tc_name} - {str(tc_info['Domain']).lower()} - {str(tc_info['Testcase_Name']).lower()}"
        sub_sc = ScenarioGenerator(name=tc_title)
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 0))
        sub_sc.add_step(self.wait_toolcase_service_down())
        sub_sc.add_step(self.wait_toolcase_service_up())
        sub_sc.add_step(self.add_sub_scenario_repeat_execution(testcase, tc_info, 1, 5))
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 2))
        return sub_sc.generate_scenario()

    def add_sub_scenario_PSPV_TCs_14874(self, testcase, tc_info):
        tc_name = testcase
        tc_title = f"{tc_name} - {str(tc_info['Domain']).lower()} - {str(tc_info['Testcase_Name']).lower()}"
        sub_sc = ScenarioGenerator(name=tc_title)
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 0))
        sub_sc.add_step(self.wait_toolcase_service_down())
        sub_sc.add_step(self.wait_toolcase_service_up())
        sub_sc.add_step(self.add_sub_scenario_repeat_execution(testcase, tc_info, 1, 50))
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 2))
        return sub_sc.generate_scenario()

    def add_sub_scenario_PSPV_TCs_9834(self, testcase, tc_info):
        tc_name = testcase
        tc_title = f"{tc_name} - {str(tc_info['Domain']).lower()} - {str(tc_info['Testcase_Name']).lower()}"
        sub_sc = ScenarioGenerator(name=tc_title)
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 0))
        sub_sc.add_step(self.wait_toolcase_service_down())
        sub_sc.add_step(self.wait_toolcase_service_up())
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 1))
        sub_sc.add_step(self.wait_toolcase_service_down())
        sub_sc.add_step(self.wait_toolcase_service_up())
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 2))
        sub_sc.add_step(self.wait_toolcase_service_down())
        sub_sc.add_step(self.wait_toolcase_service_up())
        sub_sc.add_step(self.add_sub_scenario_repeat_execution(testcase, tc_info, 3, 5))
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 4))
        return sub_sc.generate_scenario()

    def add_sub_scenario_PSPV_TCs_737(self, testcase, tc_info):
        tc_name = testcase
        tc_title = f"{tc_name} - {str(tc_info['Domain']).lower()} - {str(tc_info['Testcase_Name']).lower()}"
        sub_sc = ScenarioGenerator(name=tc_title)
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 0))
        sub_sc.add_step(self.wait_toolcase_service_down())
        sub_sc.add_step(self.wait_toolcase_service_up())
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 1))
        sub_sc.add_step(self.wait_toolcase_service_down())
        sub_sc.add_step(self.wait_toolcase_service_up())
        sub_sc.add_step(self.add_sub_scenario_repeat_execution(testcase, tc_info, 2, 5))
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 3))
        return sub_sc.generate_scenario()

    def add_sub_scenario_PSPV_TCs_761(self, testcase, tc_info):
        tc_name = testcase
        tc_title = f"{tc_name} - {str(tc_info['Domain']).lower()} - {str(tc_info['Testcase_Name']).lower()}"
        sub_sc = ScenarioGenerator(name=tc_title)
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 0))
        sub_sc.add_step(self.wait_toolcase_service_down())
        sub_sc.add_step(self.wait_toolcase_service_up())
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 1))
        sub_sc.add_step(self.wait_toolcase_service_down())
        sub_sc.add_step(self.wait_toolcase_service_up())
        sub_sc.add_step(self.add_sub_scenario_repeat_execution(testcase, tc_info, 2, 5))
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 3))
        return sub_sc.generate_scenario()

    def add_sub_scenario_PSPV_TCs_1133(self, testcase, tc_info):
        tc_name = testcase
        tc_title = f"{tc_name} - {str(tc_info['Domain']).lower()} - {str(tc_info['Testcase_Name']).lower()}"
        sub_sc = ScenarioGenerator(name=tc_title)
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 0))
        sub_sc.add_step(self.wait_toolcase_service_down())
        sub_sc.add_step(self.wait_toolcase_service_up())
        sub_sc.add_step(self.add_sub_scenario_repeat_execution(testcase, tc_info, 1, 20))
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 2))
        return sub_sc.generate_scenario()

    def add_sub_scenario_PSPV_TC_14230(self, testcase, tc_info):
        tc_name = testcase
        tc_title = f"{tc_name} - {str(tc_info['Domain']).lower()} - {str(tc_info['Testcase_Name']).lower()}"
        sub_sc = ScenarioGenerator(name=tc_title)
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 0))
        sub_sc.add_step(self.wait_toolcase_service_down())
        sub_sc.add_step(self.wait_toolcase_service_up())
        sub_sc.add_step(self.add_sub_scenario_repeat_execution(testcase, tc_info, 1, 6))
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 2))
        return sub_sc.generate_scenario()

    def add_sub_scenario_PSPV_TC_14074(self, testcase, tc_info):
        tc_name = testcase
        tc_title = f"{tc_name} - {str(tc_info['Domain']).lower()} - {str(tc_info['Testcase_Name']).lower()}"
        sub_sc = ScenarioGenerator(name=tc_title)
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 0))
        sub_sc.add_step(self.wait_toolcase_service_down())
        sub_sc.add_step(self.wait_toolcase_service_up())
        sub_sc.add_step(self.add_sub_scenario_repeat_execution(testcase, tc_info, 1, 6))
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 2))
        return sub_sc.generate_scenario()

    def add_sub_scenario_14011237817(self, testcase, tc_info):
        tc_name = testcase
        tc_title = f"{tc_name} - {str(tc_info['Domain']).lower()} - {str(tc_info['Testcase_Name']).lower()}"
        sub_sc = ScenarioGenerator(name=tc_title)
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 0))
        sub_sc.add_step(self.wait_toolcase_service_down())
        sub_sc.add_step(self.wait_toolcase_service_up())
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 1))
        sub_sc.add_step(self.wait_toolcase_service_down())
        sub_sc.add_step(self.wait_toolcase_service_up())
        sub_sc.add_step(self.add_sub_scenario_repeat_execution(testcase, tc_info, 2, 10))
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 3))
        sub_sc.add_step(self.wait_toolcase_service_down())
        sub_sc.add_step(self.wait_toolcase_service_up())
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 4))
        return sub_sc.generate_scenario()

    def add_sub_scenario_14011237851(self, testcase, tc_info):
        tc_name = testcase
        tc_title = f"{tc_name} - {str(tc_info['Domain']).lower()} - {str(tc_info['Testcase_Name']).lower()}"
        sub_sc = ScenarioGenerator(name=tc_title)
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 0))
        sub_sc.add_step(self.wait_toolcase_service_down())
        sub_sc.add_step(self.wait_toolcase_service_up())
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 1))
        sub_sc.add_step(self.wait_toolcase_service_down())
        sub_sc.add_step(self.wait_toolcase_service_up())
        sub_sc.add_step(self.add_sub_scenario_repeat_execution(testcase, tc_info, 2, 10))
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 3))
        sub_sc.add_step(self.wait_toolcase_service_down())
        sub_sc.add_step(self.wait_toolcase_service_up())
        sub_sc.add_step(self.add_sub_scenario_repeat_execution(testcase, tc_info, 4, 10))
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 5))
        return sub_sc.generate_scenario()

    def add_sub_scenario_2202183491(self, testcase, tc_info):
        tc_name = testcase
        tc_title = f"{tc_name} - {str(tc_info['Domain']).lower()} - {str(tc_info['Testcase_Name']).lower()}"
        sub_sc = ScenarioGenerator(name=tc_title)
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 0))
        sub_sc.add_step(self.wait_toolcase_service_down())
        sub_sc.add_step(self.wait_toolcase_service_up())
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 1))
        sub_sc.add_step(self.wait_toolcase_service_down())
        sub_sc.add_step(self.wait_toolcase_service_up())
        sub_sc.add_step(self.add_sub_scenario_repeat_execution(testcase, tc_info, 2, 10))
        sub_sc.add_step(self.add_sub_scenario_repeat_execution(testcase, tc_info, 3, 10))
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 4))
        return sub_sc.generate_scenario()

    def add_sub_scenario_2006737344(self, testcase, tc_info):
        tc_name = testcase
        tc_title = f"{tc_name} - {str(tc_info['Domain']).lower()} - {str(tc_info['Testcase_Name']).lower()}"
        sub_sc = ScenarioGenerator(name=tc_title)
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 0))
        sub_sc.add_step(self.wait_toolcase_service_down())
        sub_sc.add_step(self.wait_toolcase_service_up())
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 1))
        sub_sc.add_step(self.wait_toolcase_service_down())
        sub_sc.add_step(self.wait_toolcase_service_up())
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 2))
        sub_sc.add_step(self.wait_toolcase_service_down())
        sub_sc.add_step(self.wait_toolcase_service_up())
        sub_sc.add_step(self.add_sub_scenario_repeat_execution(testcase, tc_info, 3, 5))
        return sub_sc.generate_scenario()

    def add_sub_scenario_PSPV_TC_14743(self, testcase, tc_info):
        tc_name = testcase
        tc_title = f"{tc_name} - {str(tc_info['Domain']).lower()} - {str(tc_info['Testcase_Name']).lower()}"
        sub_sc = ScenarioGenerator(name=tc_title)
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 0))
        sub_sc.add_step(self.wait_toolcase_service_down())
        sub_sc.add_step(self.wait_toolcase_service_up())
        sub_sc.add_step(self.run_standalone_sub_execution_script(testcase, tc_info, 1))
        sub_sc.add_step(self.wait_toolcase_service_down())
        sub_sc.add_step(self.wait_toolcase_service_up())
        sub_sc.add_step(self.add_sub_scenario_repeat_execution(testcase, tc_info, 2, 2))
        return sub_sc.generate_scenario()
