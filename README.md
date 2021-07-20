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
    
(venv) C:\Automation\wss-autoflow\standalone>store --help
Usage: store [OPTIONS] COMMAND [ARGS]...

  Set of Test Execution scripts and commands to assist in the automated interaction
  with commonly-used execution-related activities.

Options:
  --help  Show this message and exit.

Commands:
  onemapcli      Run the Test Execution
  standalonecli  Run the Test Execution