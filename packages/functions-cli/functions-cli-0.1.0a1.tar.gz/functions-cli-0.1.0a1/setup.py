# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['functions', 'functions.commands']

package_data = \
{'': ['*']}

install_requires = \
['docker>=5.0.2,<6.0.0', 'pydantic>=1.8.2,<2.0.0', 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['functions = functions.main:app']}

setup_kwargs = {
    'name': 'functions-cli',
    'version': '0.1.0a1',
    'description': '',
    'long_description': '# `functions-cli`\n\nRun script to executing, testing and deploying included functions.\n\n**Usage**:\n\n```console\n$ functions-cli [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `build`\n* `gcp`: Deploy functions in GCP\n* `list`: List existing functions\n* `new`: Factory method for creating new functions\n* `remove`\n* `run`: Start a container for a given function\n* `stop`\n\n## `functions-cli build`\n\n**Usage**:\n\n```console\n$ functions-cli build [OPTIONS] FUNCTION_PATH\n```\n\n**Arguments**:\n\n* `FUNCTION_PATH`: Path to the functions you want to build  [required]\n\n**Options**:\n\n* `--force`: [default: False]\n* `--help`: Show this message and exit.\n\n## `functions-cli gcp`\n\nDeploy functions in GCP\n\n**Usage**:\n\n```console\n$ functions-cli gcp [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `delete`: Deletes a functions deployed to GCP\n* `deploy`: Deploy a functions to GCP\n* `describe`: Returns information about a deployed function\n* `install`: Install required libraries\n* `logs`: Reads log from a deployed function\n* `update`: Update required libraries\n\n### `functions-cli gcp delete`\n\nDeletes a functions deployed to GCP\n\n**Usage**:\n\n```console\n$ functions-cli gcp delete [OPTIONS] FUNCTION_NAME\n```\n\n**Arguments**:\n\n* `FUNCTION_NAME`: Name of the function you want to remove  [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n### `functions-cli gcp deploy`\n\nDeploy a functions to GCP\n\n**Usage**:\n\n```console\n$ functions-cli gcp deploy [OPTIONS] FUNCTION_DIR\n```\n\n**Arguments**:\n\n* `FUNCTION_DIR`: Path to the functions you want to deploy  [required]\n\n**Options**:\n\n* `--service [cloud_function]`: Type of service you want this resource to be deploy to\n* `--help`: Show this message and exit.\n\n### `functions-cli gcp describe`\n\nReturns information about a deployed function\n\n**Usage**:\n\n```console\n$ functions-cli gcp describe [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n### `functions-cli gcp install`\n\nInstall required libraries\n\n**Usage**:\n\n```console\n$ functions-cli gcp install [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n### `functions-cli gcp logs`\n\nReads log from a deployed function\n\n**Usage**:\n\n```console\n$ functions-cli gcp logs [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n### `functions-cli gcp update`\n\nUpdate required libraries\n\n**Usage**:\n\n```console\n$ functions-cli gcp update [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `functions-cli list`\n\nList existing functions\n\n**Usage**:\n\n```console\n$ functions-cli list [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `functions-cli new`\n\nFactory method for creating new functions\n\n**Usage**:\n\n```console\n$ functions-cli new [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `http`: Creates a new http directory\n* `pubsub`: Creates a new pubsub directory\n\n### `functions-cli new http`\n\nCreates a new http directory\n\n**Usage**:\n\n```console\n$ functions-cli new http [OPTIONS] FUNCTION_NAME\n```\n\n**Arguments**:\n\n* `FUNCTION_NAME`: Name of a function in alphabetic constrain [i.e new-function]  [required]\n\n**Options**:\n\n* `--dir PATH`: Directory that will be used as a root of the new function\n* `--help`: Show this message and exit.\n\n### `functions-cli new pubsub`\n\nCreates a new pubsub directory\n\n**Usage**:\n\n```console\n$ functions-cli new pubsub [OPTIONS] FUNCTION_NAME\n```\n\n**Arguments**:\n\n* `FUNCTION_NAME`: Name of a function in alphabetic constrain [i.e new-function]  [required]\n\n**Options**:\n\n* `--dir TEXT`: Directory that will be used as a root of the new function\n* `--help`: Show this message and exit.\n\n## `functions-cli remove`\n\n**Usage**:\n\n```console\n$ functions-cli remove [OPTIONS] FUNCTION_NAME\n```\n\n**Arguments**:\n\n* `FUNCTION_NAME`: Name of the function you want to remove  [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `functions-cli run`\n\nStart a container for a given function\n\n**Usage**:\n\n```console\n$ functions-cli run [OPTIONS] FUNCTION_NAME\n```\n\n**Arguments**:\n\n* `FUNCTION_NAME`: Name of the function you want to run  [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `functions-cli stop`\n\n**Usage**:\n\n```console\n$ functions-cli stop [OPTIONS] FUNCTION_NAME\n```\n\n**Arguments**:\n\n* `FUNCTION_NAME`: Name of the function you want to stop  [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n',
    'author': 'Katolus',
    'author_email': 'pkatolik@healthshare.com.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
