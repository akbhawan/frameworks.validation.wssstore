"""
1. Testlist based on phase is generated from pyOneBKC
2. Generated testlist is passed to RAILS to generate scenario json
3. Scenario json is passed to TWS post scenario to execute testcases
"""
import click
from logger.logger_util import get_logger_instance
from standaloneapi.run_api import RunScenarioAPI

LOG = get_logger_instance()


@click.group("standalone")
def main():
    """ Run the Test Execution"""
    return 0


@main.command('generate_scenario', context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.pass_context
@click.option("--testcases", "-tc", help='Mention the local file path')
@click.option("-timeout", "-to", type=float, default=3.0,
              help='Timeout(in hrs) to stop TWS scenario if not initiated, '
                   'by default timeout will be 8hrs')
def generate_onemap_scenario(
        ctx,
        testcases: str,
        timeout: float
):
    """Select testlist based on phase and generate scenario json using RAILS"""
    LOG.debug("********* af run tests Params *********")
    solunk_kwargs = {(ctx.args[i][2:] if str(ctx.args[i]).startswith("--") else
               ctx.args[i][1:]): ctx.args[i+1] for i in range(0, len(ctx.args), 2)}
    LOG.info(f"Splunk MetaData: {solunk_kwargs}")
    LOG.info(f"Test Cases: {testcases}")
    getRunScenario = RunScenarioAPI(
        framework="standalone",
        testcases=testcases,
        timeout=timeout,
        splunk_metadata=solunk_kwargs
    )
    results = getRunScenario.generate_standalone_scenario()
    # if results.get('status') == 'Success':
    #     return_run_test_response(results)
    # else:
    #     LOG.error("Failed to trigger test execution")
    #     response = {'provision_type': 'WSS-STORE',
    #                 'sut': None,
    #                 'result_url': results.get('message'),
    #                 'status': 'Failure'}
    #     return_run_test_response(response)
    return results

def return_run_test_response(response):
    """
    Return Run Test Provision response
    :param response:
    :return:
    """
    if response.get('status') != 'Failure':
        LOG.info(f"Success: {response.get('provision_type')} test execution "
                 f"successfully completed on {response.get('sut_name')}")
        LOG.info(f"Execution Url: {response.get('result_url')}")
        LOG.debug("---------------------------------------------------------"
                  "---------------------------------------------------------"
                  "-------\n")
    else:
        LOG.error(
            f"Failed: {response.get('provision_type')} test execution on {response.get('sut_name')}")
        LOG.error(f"Details: {response.get('result_url')}")
        LOG.debug("---------------------------------------------------------"
                  "---------------------------------------------------------"
                  "-------\n")

