# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ra_fixture_generator']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'mimesis>=4.1.3,<5.0.0',
 'pydantic>=1.8.1,<2.0.0',
 'ra-flatfile-importer>=0.1.2,<0.2.0',
 'ra-utils>=0.4.0,<0.5.0',
 'ramodels>=2.1.1,<3.0.0']

setup_kwargs = {
    'name': 'ra-fixture-generator',
    'version': '0.2.0',
    'description': 'Flatfile Fixture generator for OS2mo/LoRa',
    'long_description': '<!--\nSPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>\nSPDX-License-Identifier: MPL-2.0\n-->\n\n\n# RA Fixture Generator\n\nOS2mo/LoRa Flatfile Fixture Generator.\n\n## Usage\n```\ndocker build . -t ra-fixture-generator\n```\nWhich yields:\n```\n...\nSuccessfully built ...\nSuccessfully tagged ra-fixture-generator:latest\n```\nAfter which you can run:\n```\ndocker run --rm ra-fixture-generator --help\n```\nWhich yields:\n```\nUsage: fixture_generator.py [OPTIONS]\n\n  Flatfile Fixture Generator.\n\n  Used to generate flatfile fixture data (JSON) for OS2mo/LoRa.\n\nOptions:\n  --name TEXT           Name of the root organization  [required]\n  --indent INTEGER      Pass \'indent\' to json serializer\n  --lora-file FILENAME  Output Lora Flatfile  [required]\n  --mo-file FILENAME    Output OS2mo Flatfile  [required]\n  --help                Show this message and exit.\n```\nAt this point two flat files can be generated with:\n```\ndocker run --rm -v $PWD:/srv/ ra-fixture-generator \\\n    --name "Aarhus Kommune" --lora-file /srv/lora.json --mo-file /srv/mo.json\n```\nAt which point two files `lora.json` and `mo.json` will be available in the current work-dir.\nThese files can then be uploaded using the `ra-flatfile-importer`.\n\nFor instance using:\n```\ndocker run -i --rm ra-flatfile-importer lora upload --mox-url http://MOXURL:8080 < lora.json\ndocker run -i --rm ra-flatfile-importer mo upload --mo-url http://MOURL:5000 < mo.json\n```\n\nAlternatively the two can be combined:\n```\ndocker run -i --rm ra-fixture-generator \\\n    --name "Aarhus Kommune" --lora-file - --mo-file /dev/null | \\\ndocker run -i --rm ra-flatfile-importer lora upload --mox-url http://MOXURL:8080\n```\nAnd similarily for MO:\n```\ndocker run -i --rm ra-fixture-generator \\\n   --name "Aarhus Kommune" --lora-file /dev/null --mo-file - | \\\ndocker run -i --rm ra-flatfile-importer mo upload --mo-url http://MOURL:5000\n```\n\n\n## Versioning\nThis project uses [Semantic Versioning](https://semver.org/) with the following strategy:\n- MAJOR: Incompatible changes to existing data models\n- MINOR: Backwards compatible updates to existing data models OR new models added\n- PATCH: Backwards compatible bug fixes\n\n<!--\n## Getting Started\n\nTODO: README section missing!\n\n### Prerequisites\n\n\nTODO: README section missing!\n\n### Installing\n\nTODO: README section missing!\n\n## Running the tests\n\nTODO: README section missing!\n\n## Deployment\n\nTODO: README section missing!\n\n## Built With\n\nTODO: README section missing!\n\n## Authors\n\nMagenta ApS <https://magenta.dk>\n\nTODO: README section missing!\n-->\n## License\n- This project: [MPL-2.0](LICENSES/MPL-2.0.txt)\n- Dependencies:\n  - pydantic: [MIT](LICENSES/MIT.txt)\n\nThis project uses [REUSE](https://reuse.software) for licensing. All licenses can be found in the [LICENSES folder](LICENSES/) of the project.\n',
    'author': 'Magenta',
    'author_email': 'info@magenta.dk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://magenta.dk/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
