"""
Set of AutoFlow scripts and commands to assist in
the automated interaction with commonly-used
execution-related activities.
"""
import sys
import logging
from pathlib import Path

# 3rd party modules
import click

"""Set of AutoFlow scripts and commands to assist in
the automated interaction with commonly-used
execution-related activities.

Returns:
    commands -- List of available commands to execute
"""

"""
Click Code, recomendenation and guideance for click interface implementation is provided by Zach Habermann!
Thanks Zach!!

"""

BASE_SCRIPT_DIR = Path(__file__).parent
BASE_SCRIPT_NAME = Path(__file__).name
EXCLUDES = [BASE_SCRIPT_NAME, '__init__.py']


# https://click.palletsprojects.com/en/7.x/commands/#custom-multi-commands
class CliLoader(click.MultiCommand):
    """
    Code taken from https://click.palletsprojects.com/en/7.x/commands/#custom-multi-commands
    Any click module/group containing a 'main' entry point will get picked up by this parent module
    """

    def list_commands(self, ctx, base_script_dir=BASE_SCRIPT_DIR, exclusions=EXCLUDES):
        scripts = []
        for filename in Path(base_script_dir).rglob('*.py'):
            if filename.suffix == ".py" and filename.name not in exclusions:
                scripts.append(filename.stem)
        scripts.sort()
        return scripts

    def get_command(self, ctx, name, base_script_dir=BASE_SCRIPT_DIR, hook='main'):
        script = {}
        click_file = Path(base_script_dir, name + '.py')
        try:
            _evaluate_file(script, click_file)
        except NameError as error:
            logging.warning(f"Unable to load {click_file.name}. Missing module {error}")
            return None
        except ModuleNotFoundError as error:
            logging.warning(f"Unable to load {click_file.name}. {error}")
            return None
        except FileNotFoundError as error:
            logging.warning(f"Unable to load {click_file.name}. {error}")
            return None

        if hook not in script:
            logging.warning(
                f"Unable to load {click_file.name}. Missing required entry point: '{hook}'"
            )
            return None

        return script[hook]


def _evaluate_file(script, click_file):
    with open(click_file) as f_handle:
        code = compile(f_handle.read(), click_file, 'exec')
        eval(code, script, script)


@click.command('store', cls=CliLoader)
@click.pass_context
def main(ctx):
    """Set of AutoFlow scripts and commands to assist in
        the automated interaction with commonly-used
        execution-related activities.
    """
    ctx.obj = {}


if __name__ == "__main__":
    sys.exit(main(None))
