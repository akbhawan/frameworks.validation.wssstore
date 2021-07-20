from setuptools import setup, find_packages
import os

TEST_REQUIREMENTS = ['bandit', 'pytest==5.4.3', 'pytest-cov', 'pylint', 'pyfakefs']
INSTALL_REQUIREMENTS = ['click', 'requests', 'python-dotenv', 'colorlog']

# with open(os.path.join('cmake', 'version'), 'r') as fd:
#     version = fd.read().strip()

setup(name='standaloneapi',
    version="1.0",
    description="WSS-STORE standalone & onemap apis to generate TWS Scenario",
    author='Anil Bhawangirkar',
    author_email='anil.k.bhawangirkar@intel.com',
    packages=find_packages(),
    include_package_data=True,
    scripts=[
        'cli_scripts/store.py',
        "cli_scripts/onemap.py",
        "cli_scripts/standalone.py"
    ],
    entry_points={
        'console_scripts': [
            'store=cli_scripts.store:main'
        ]
    },
    install_requires=INSTALL_REQUIREMENTS,
    extras_require={
        'test': TEST_REQUIREMENTS
    }
    )
