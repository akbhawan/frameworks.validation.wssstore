# WSS-STORE Test Execution API's initiative

<p align="left">
  <a href="https://github.com/intel-sandbox/frameworks.design.software.dbio.code-quality-moonshot/actions/workflows/ci.yaml?query=branch%3Amain">
    <img alt="Build" src="https://github.com/intel-sandbox/frameworks.design.software.dbio.code-quality-moonshot/actions/workflows/ci.yaml/badge.svg"></a>
</p>

## About

  1. Clone the code 
      git clone https://github.com/akbhawan/frameworks.validation.wssstore.git

  2. Create virtual enviornment 
      py -m venv venv
      venv\Scripts\activate

  3. Run "pip install -e ".[test]" --proxy=http://proxy-chain.intel.com:911"

  4. Run "store --help"

## WSS-STORE CLI Commands
  (venv) C:\Automation\wss-autoflow\standalone>store --help
  Usage: store [OPTIONS] COMMAND [ARGS]...

  Set of Test Execution scripts and commands to assist in the automated interaction
  with commonly-used execution-related activities.

  Options:
  --help  Show this message and exit.

  Commands:
  ### onemap      Run the Test Execution
  ### standalone  Run the Test Execution

  (venv) C:\Automation\wss-autoflow\frameworks.validation.wssstore>store standalone generate_scenario --help
  Usage: store standalone generate_scenario [OPTIONS]

  Select testlist based on phase and generate scenario json using RAILS

  Options:
  -tc, --testcases TEXT  Mention the local file path
  -timeout, -to FLOAT    Timeout(in hrs) to stop TWS scenario if not
                         initiated, by default timeout will be 8hrs
  --help                 Show this message and exit.
  
  
## Commands:
  Standalone:
  store standalone generate_scenario -tc "PSPV-TC-14405,PSPV-TC-14078"

  OneMap:
      store onemap generate_scenario -tc "16011968858,16011968881"
    
## Output JSON Path:
  {Working Directory}/AF_Output
