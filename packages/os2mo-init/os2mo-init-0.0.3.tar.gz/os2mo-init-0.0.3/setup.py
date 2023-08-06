# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['os2mo_init']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'ra-utils>=0.4.0,<0.5.0', 'raclients>=0.4.3,<0.5.0']

setup_kwargs = {
    'name': 'os2mo-init',
    'version': '0.0.3',
    'description': 'Database initialiser for OS2mo',
    'long_description': "<!--\nSPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>\nSPDX-License-Identifier: MPL-2.0\n-->\n\n# OS2mo Init\n\nOS2mo Initialiser.\n\n## Build\n```\ndocker build . -t os2mo-init\n```\nWhich yields:\n```\n...\nSuccessfully built ...\nSuccessfully tagged os2mo-init:latest\n```\nAfter which you can run:\n```\ndocker run --rm os2mo-init --help\n```\nWhich yields:\n```\nUsage: __main__.py [OPTIONS]\n\nOptions:\n  --lora-url TEXT              Address of the LoRa host  [env var: LORA_URL;\n                               default: http://localhost:8080]\n\n  --root-org-name TEXT         Name of the root organisation  [env var:\n                               ROOT_ORG_NAME; default: Magenta Aps]\n\n  --municipality-code INTEGER  Municipality code of the root organisation\n                               [default: 1234]\n\n  --help                       Show this message and exit.\n\n  In addition to the listed environment variables, the program accepts\n  parameters from environment variables using the format\n  'OS2MO_INIT_<OPTION>'; for example 'OS2MO_INIT_MUNICIPALITY_CODE'.\n  Furthermore, the following environment variables are used to establish a\n  connection to LoRa:\n\n  CLIENT_ID [default: mo]\n  CLIENT_SECRET [required]\n  AUTH_REALM [default: lora]\n  AUTH_SERVER [default: http://localhost:8080/auth]\n```\n\n## Usage\nThe primary usage of the tool is to initialise OS2mo's LoRa database.\n```\ndocker run --rm os2mo-init --client-secret='hunter2'\n```\n\n## Versioning\nThis project uses [Semantic Versioning](https://semver.org/) with the following strategy:\n- MAJOR: Incompatible changes to existing commandline interface\n- MINOR: Backwards compatible updates to commandline interface\n- PATCH: Backwards compatible bug fixes\n\nThe fileformat is versioned directly, and the version is exported in the file itself.\n\n<!--\n## Getting Started\n\nTODO: README section missing!\n\n### Prerequisites\n\n\nTODO: README section missing!\n\n### Installing\n\nTODO: README section missing!\n\n## Running the tests\n\nTODO: README section missing!\n\n## Deployment\n\nTODO: README section missing!\n\n## Built With\n\nTODO: README section missing!\n\n## Authors\n\nMagenta ApS <https://magenta.dk>\n\nTODO: README section missing!\n-->\n## License\n- This project: [MPL-2.0](LICENSES/MPL-2.0.txt)\n\nThis project uses [REUSE](https://reuse.software) for licensing. All licenses can be found in the [LICENSES folder](LICENSES/) of the project.\n",
    'author': 'Magenta',
    'author_email': 'info@magenta.dk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://magenta.dk/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
