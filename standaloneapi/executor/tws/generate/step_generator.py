"""
Module to build tws steps.
"""


class StepGenerator:

    def __init__(self, **kwargs):
        """
        Initialize Step Generator Class.
        :param kwargs:
        """
        self._name = kwargs.get('name')
        self._timeout = kwargs.get('timeout') if kwargs.get('timeout') else 300
        self._critical = False
        self._alwaysPasses = False
        self._ignoreResults = False
        self._executeInBackground = False
        self._disabled = False
        self._dependency = None
        self._logPath = None
        self._variables = dict()
        self._defaults = dict()
        self._type = "subprocess"
        self._executable = "%python-path%"
        self._cwd = None
        self._waitBeforeExecutionTime = None
        self._requiresDict = dict()
        self._requiresDict["named_req"] = "SUT"
        self._transition = None
        self._min = None
        self._max = None
        self._serviceFilters = None
        self._metaAddress = None
        self._parameters = None
        self._wait_post = None
        self.stderrnotmatches = None
        self._resumewaitprocess = None
        self._logupdateinterval = None
        self._resumelogpath = None

    def setRequiresDict(self, system):
        """Set Requires Dict"""
        self._requiresDict["named_req"] = system

    def setstderrnotmatches(self,value):
        self.stderrnotmatches = value

    def getstderrnotmatches(self):
        return self.stderrnotmatches

    def domain(self):
        """ Get Domain"""
        return self._domainEnum

    def wait_pre(self):
        """Get wait_pre param"""
        return self._waitBeforeExecutionTime

    def executeinbackground(self):
        """Get executionbackground param"""
        return self._executeInBackground

    def cwd(self):
        """get cwd"""
        return self._cwd

    def setExecutable(self, _executable):
        """Set Executable."""
        self._executable = _executable

    def setVariables(self, variables):
        """Set Variables."""
        self._variables = variables

    def setDefaults(self, defaults):
        """Set Defaults"""
        self._defaults = defaults

    def setWaitPost(self, wait_post):
        """Wait post"""
        self._wait_post = wait_post

    def type(self):
        """Get Type Ex. TWS"""
        return self._type

    def setType(self, value):
        """Set Type Param"""
        self._type = value

    def parameters(self):
        """get tws parameters"""
        return self._parameters

    def executeInBackground(self):
        """Get executionBackground param info"""
        return self._executeInBackground

    def disabled(self):
        """Get tws disabled info"""
        return self._disabled

    def setCwd(self, cwd):
        """Set cwd info."""
        self._cwd = cwd

    def setExecuteInBackground(self, aBool):
        """Set ExecutionBackground Info."""
        self._executeInBackground = aBool

    def setTimeout(self, anInt):
        """Set timeout param"""
        self._timeout = anInt

    def timeout(self):
        """Get Timeout info"""
        return self._timeout

    def setParameters(self, aString):
        """Set TWS Params"""
        self._parameters = aString

    def alwayspasses(self):
        """ AlwaysPass attribute Info"""
        return self._alwaysPasses

    def ignore_results(self):
        """Get ingnore results info"""
        return self._ignoreResults

    def setAlwaysPasses(self, alwaysPasses):
        """Set AlwaysPass attribute Info."""
        self._alwaysPasses = alwaysPasses

    def setIgnoreResults(self, ignoreResults):
        """SetIgnoreResultsInfo params"""
        self._ignoreResults = ignoreResults

    def setWaitBeforeExecutionTime(self, anInt):
        """Set setWaitBeforeExecutionTime Param"""
        self._waitBeforeExecutionTime = anInt

    def setCritical(self, critical):
        """Set Critical."""
        self._critical = critical

    def critical(self):
        """ Fetch Critical"""
        return self._critical

    def setTransition(self, transition):
        """Set Transition"""
        if transition is not None:
            self._transition = transition

    def transition(self):
        """Get Transition param info."""
        return self._transition

    def setMetaAddress(self, meta_address):
        """Set Meta Address"""
        if meta_address is not None:
            self._metaAddress = meta_address

    def meta_address(self):
        """Get Meta Address"""
        return self._metaAddress

    def setResumeWaitProcess(self, resumewaitprocess):
        """Get resume wait process"""
        self._resumewaitprocess = resumewaitprocess

    def setResumeWait(self, resumewait):
        """Get resume wait"""
        self._logupdateinterval= resumewait

    def setResumeLogPath(self, resumelogpath):
        """Get resume wait"""
        self._resumelogpath = resumelogpath

    def generate_tws_step_json(self):
        """template for generating tws step json"""
        step = {
            "name": self._name,
            "tags": "",
            "type": self._type,
            "requires": self._requiresDict,
            "variables": self._variables,
            "executable": self._executable,
            "parameters": self._parameters,
            "defaults": self._defaults,
            "disabled": False,
            "critical": self._critical,
            "timeout": self._timeout,
            "alwayspasses": self._alwaysPasses
        }
        if self._cwd:
            step["cwd"] = self._cwd
        if self._waitBeforeExecutionTime:
            step["wait_pre"] = self._waitBeforeExecutionTime
        if self._wait_post:
            step["wait_post"] = self._wait_post
        if self.stderrnotmatches:
            step['stderrnotmatches'] = self.stderrnotmatches
        if self._logupdateinterval:
            step['logupdateinterval'] = self._logupdateinterval
        if self._resumewaitprocess:
            step['resumewaitprocess'] = self._resumewaitprocess
        if self._resumelogpath:
            step['resumelogpath'] = self._resumelogpath

        return step
