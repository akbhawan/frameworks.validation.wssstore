Autoflow: 

Autoflow is the next generation set of scripts for running automated system testing.


Installation Steps: 

1) Open the folder where you want to clone the project. Right click > Git Bash here. Or open command     prompt
$git clone ssh://git@gitlab.devtools.intel.com:29418/OWR/Test/autoflow.git                 

2) Change the current working directory to 'autoflow' (This autoflow folder is referred to as the ‘root directory’ in this document)
$cd autoflow 

3) Run git fetch
$git fetch

4) Switch to 'develop' branch
     Right now the code base needs to be pulled from develop branch
$git checkout develop  

5) Create virtual environment (Run these commands in command prompt, under  the root directory)
$py -m venv env

6) And activate the virtual environment 
$env\scripts\activate


$git clone ssh://git@gitlab.devtools.intel.com:29418/OWR/Test/autoflow.git                 
$cd autoflow 
$git fetch
$git checkout develop  
$py -m venv env 
$env\scripts\activate



7) $pip install -e ".[test]" --proxy=http://proxy-chain.intel.com:911


Validating the Installation

After install, run automation flow by running the command as below 
$ af --help 

Optional step: this will ensure that all the unit tests are running 
$pytest test  


Setup SUT

From the root directory cd autoflow\collateral\
Specify your SUT, HOST, controller, location details as shown below. 
You can edit the CSV file in excel

autoflow\collateral\sut_info.csv 

Phase: can be bronze or silver or rails or QAC 
Location: US or BA 
Controller: Name of the Controller (Eg: BASTWSPROD14)
Sut: Name of the SUT  (Eg: CMLURAILS06)
Platform: Platform name (Eg: CML)
 

Setup - TWS 

Install TWS from 
http://ubitws.intel.com/downloads/TWS_Zips/ 

Setup – Python27

1.	Download python2.7.8 from https://www.python.org/downloads/release/python-278/
2.	Download pip file from https://bootstrap.pypa.io/get-pip.py to your workspace
3.	Make sure you set proxy as below before running get-pip.py:
SET http_proxy=http://proxy-chain.intel.com:911
SET https_proxy=http://proxy-chain.intel.com:912
4.	Execute get-pip.py using python2.7.8: <python2_path>\python.exe get-pip.py
Example: C:\Python27\python.exe get-pip.py

5.	After successful python27 installation - >  Edit config.ini and change the python path according to the setup in your machine.

Setup Config.ini 
Open config.ini file (config.ini file is present in the root directory.)
Ensure that the following paths are correctly mentioned in config.ini file, as per the setup in your machine.

1.	[TWS]
tws_path = C:\tws_2.13.2

 

2.	[RAILS]
python_path = C:\Python27\python.exe

 

User Guide

Commands:

$af fetch –help 
$af provision –help 
$af run –help 

Fetching the tests from HSD
$af fetch tests --phase=bronze --execution_config="platform.Comet Lake.cmls-gt2-cmph-dt-CML-S-CMP-H-20H1"

or 

$af fetch tests --phase=bronze --username=idsid --password=password 


$af fetch sut  --platform=CML --location=BA --phase=rails

