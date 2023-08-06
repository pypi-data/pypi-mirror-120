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
    'version': '0.1.0a3',
    'description': 'CLI tool for managing your FaaS repositories',
    'long_description': "# This package that will get you working with FaaS\n\n|   !   | This package is not anywhere near being ready. It hasn't been released in any major or minor versions of it yet as it is constant development. Use it at your own risk and pleasure. |\n| :---: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |\n\n<!-- ![Logo]() -->\n\n\n\n`functions-cli` is a utility package written in Python. It is built to help the developer code, test and deploy FaaS (Function as a Service) resources. \n\nIt is using `docker` to build and orchestrate the functions locally. To deploy them to any of the cloud providers you need to have relevant software installed and appropriate authorization to deploy them. \n\n## Compatibility\n\n- Currently the project has been developed and tested only on a Linux OS with **Python 3.9** as the deployment environment.  \n\n## Requirement\n\nThe package is a utility one and it requires underlying software for specific function to be available. \n\n- Python >= 3.9 - for the functioning of the package. \n- `gcloud` - for deploying to the GCP environment.\n- `docker` - for running any of the functions locally.\n- `poetry` - for running the source code locally. \n\n## Installation\n\nSince it is a regular Python package you can start using it simply by installing the package in your Python environment by running\n\n```console\npip install functions-cli\n```\n\nin your console.\n\n### Running from source code\n\nTo operate the package from the source code. \n\n1. Download the repository.\n2. Using `poetry`, install all the dependencies by running `poetry install`. \n3. Run `poetry shell` to enter the scope of the package.\n4. Execute or invoke the commands like you would normally, by running `functions [OPTIONS] COMMAND [ARGS] ...` in the invoked shell. \n\n**Additionally** you can install the package from source code by building a wheel and installing it manually in your environment's scope. \n\n5. Run `poetry build` and you should see a `dist` folder appear in the root directory of the code (assuming you are running the command from there).\n6. Install the package directly by the while specifying a path to the source - `pip install /home/{your_user}/{project_root_path}/dist/functions_cli-0.1.0a2-py3-none-any.whl`. \n\nHandy tutorial in the scope of the `typer` package, that could help with this -> [here](https://typer.tiangolo.com/tutorial/package/). \n\n## Usage\n\nRegardless if you installed the package from the online repository or from the source code, you should be able to invoke the `functions` tool from your command line. The tool has many different commands that should help you building your serverless functions (surprise, otherwise it would be useless...). Here I name a few core ones, but for a full and a comprehensive description of the `CLI` please refer to the [cli document](docs/cli.md).\n\nKeep in mind that the package is in development and all of its structure is a subject to change. \n\n## Creating a new FaaS\n\nThe tool allows you to quickly generate a template of a function that you can the modify to quicken your efforts in producing code. \n\n```console\nfunctions new http {new_of_the_function}\n```\n\nwill generate you a new http like template for your FaaS function in your current directory.\n\n## Running a function locally\n\nA lot of us want to see and feel what we have created working first before we deploy it to the world. Running...\n\n```console\nfunctions run {name_of_the_function}\n```\n\nwill start a docker container and expose it to your locally network on a available port. \n\n**Note**: If you haven't run this function before it will ask you to build (the build command) the function first before running. # To be added...\n\nPlease remember that the container will run as long as you leave it for, so make sure to take it down once you have done all your testing. Running...\n\n```\nfunctions stop {name_of_the_function}\n```\n\nshould do the job.\n\n## Deployment it to the cloud\n\nSince we build software to serve us something, we most likely want to deploy it to see it all working and get that developer satisfaction. \n\nDepending whether you have a configuration set up you will be able to deploy your projects to various platforms (support pending). \n\nFor example to deploy a function quickly to GCP as a cloud function you want to run...\n\n```console\nfunctions gcp deploy {path_to_the_function}\n```\n\nWith the correct setup and permissions this should allow you to the deploy a function to the GCP directly from the `functions` cli.  \n\n## Getting help\n\nThe tool is built on brilliant software of others. One of them being `typer`. This allows you to query the CLI for any useful information by adding `--help` to any of your commands (useful tip to all your future work). \n\n```console\nfunctions run --help\n```\n\nIf you stumble in to any major issue that is not described in the documentation, send me a message. I will try to assist when possible.",
    'author': 'Katolus',
    'author_email': 'katolus.work@gmail.com',
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
