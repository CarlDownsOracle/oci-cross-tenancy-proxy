import io
import logging
import os
import subprocess

from fdk import response

# Set all registered loggers to the configured log_level

logging_level = os.getenv('LOGGING_LEVEL', 'INFO')
loggers = [logging.getLogger()] + [logging.getLogger(name) for name in logging.root.manager.loggerDict]
[logger.setLevel(logging.getLevelName(logging_level)) for logger in loggers]


def handler(ctx, data: io.BytesIO = None):
    """
    :param ctx: Fn Context
    :param data: Payload
    :return: JSON Response from CLI output
    """

    try:
        command = data.getvalue()
        logging.getLogger().info(f'{ctx.FnName()} / logging level / {logging_level}')
        logging.getLogger().info(f'command / {command}')
        fn_response = run_cli(command.decode('utf-8'))
        logging.getLogger().debug(f"response / {fn_response}")

    except (Exception, ValueError) as e:
        logging.getLogger().exception(e)
        fn_response = {"exception": str(type(e)), "error": str(e)}

    return response.Response(
        ctx, response_data=fn_response,
        headers={"Content-Type": "application/json"}
    )


def run_cli(command: str):
    """
    :param command: calls oci cli with this command
    :return: stdout and stderr
    """

    if command is None:
        logging.debug('cli command / not provided')
        return None

    # if the cli command starts with 'oci ':
    # strip for convenience.

    if command.startswith('oci '):
        logging.debug('removing "oci " command prefix.')
        command = command[4:]

    # if the required --auth declaration is not present:
    # add it for convenience.

    if '--auth ' not in command:
        logging.debug('appending "--auth resource_principal" to cli command.')
        command = f'{command} --auth resource_principal'

    invoke = f'python cli.py {command}'
    completed = subprocess.run(invoke, shell=True, capture_output=True, check=False)

    std_out = completed.stdout.decode('utf8')
    std_error = completed.stderr.decode('utf8')

    if completed.returncode != 0:
        logging.error(f'cli error / return code / {completed.returncode}')

    return f'{std_out}{std_error}'
