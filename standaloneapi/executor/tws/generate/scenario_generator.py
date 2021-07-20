import json


class ScenarioGenerator:
    """Scenario to hold the steps(toolcases in TWS)"""
    document = None
    name = None

    def __init__(self, **kwargs):
        """
        Create instance with Scenario `name` and expect rest of the scenario
        properties from YAML document added at runtime to the instance

        :param name: Name of the Scenario
        """
        self.name = kwargs.get('name')
        self.tools = []
        self.type = 'TWS'
        self.repetitions = 1
        self.tags = ""
        self.variables = dict()
        self.metadata = {}
        self.collateral = []
        self.execution_data = dict()
        self.collateral = []
        self.critical = False
        self.defaults = dict()
        self.scenario_hooks = []
        self.sut = kwargs.get('sut')
        self.host = kwargs.get('host') if kwargs.get('host') else "%SUT.host%"
        self.requires = []

    def setRequires(self, requires):
        """Set Requires Dict"""
        self.requires = requires

    def setRepetation(self, repetitions):
        """Set repetitions Dict"""
        self.repetitions = repetitions

    def setRequiresController(self):
        requires_controller = {
                "controller": "true",
                "named_req": "Controller",
                "reserve": False,
                "service_id": "*"
            }
        self.requires.append(requires_controller)

    def setRequiresSut(self):
        requires_sut = {
                "named_req": "SUT",
                "reserve": True,
                "service_id": str(self.sut).strip()
            }
        self.requires.append(requires_sut)

    def setRequiresHost(self):
        requires_host = {
            "named_req": "HOST",
            "reserve": True,
            "service_id": str(self.host).strip()
        }
        self.requires.append(requires_host)

    def getVariables(self):
        """Get Variables."""
        return self.variables

    def setVariables(self, variables):
        """Set Variables"""
        self.variables = variables

    def getExecutionData(self):
        """Get Execution Data."""
        execution_data = {}
        return execution_data

    def setExecutionData(self, execution_data):
        """Set Execution Data"""
        self.execution_data = execution_data

    def setDefaults(self, defaults):
        """Set Defaults"""
        self.defaults = defaults

    def setCritical(self, critical):
        """Set Critical"""
        self.critical = critical

    def add_step(self, step):
        """
        Add each step to form list of `steps`

        :param step: A single toolcase/Sub-Scenario
        """
        self.tools.append(step)
        return self.tools[-1]

    def generate_scenario(self):
        """Generate Scenario Template Structure."""
        Scenario = {
            "name": self.name,
            "tags": self.tags,
            "metadata": self.metadata,
            "type": self.type,
            "repetitions": self.repetitions,
            "requires": self.requires,
            "execution_data": self.execution_data,
            "collateral": self.collateral,
            "variables": self.variables,
            "critical": self.critical,
            "defaults": self.defaults,
            "scenario_hooks": self.scenario_hooks,
            "tools": self.tools
        }
        return Scenario

    def convert_dict_to_json(self, dict_obj):
        """Converts any python dictionary into a json"""
        json_obj = json.dumps(dict_obj, indent=4)
        return json_obj

    def write_scenario_to_file(self, content, file_name):
        """Write Scenario to File Path."""
        with open(file_name, "w") as sc_json_file:
            sc_json_file.write(content)
