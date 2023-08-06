# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['paypi']
install_requires = \
['gql[aiohttp]==3.0.0a6']

setup_kwargs = {
    'name': 'paypi',
    'version': '1.0.6',
    'description': 'Official PayPI Partner Library',
    'long_description': '[![Contributors][contributors-shield]][contributors-url]\n[![Forks][forks-shield]][forks-url]\n[![Stargazers][stars-shield]][stars-url]\n[![Issues][issues-shield]][issues-url]\n[![MIT License][license-shield]][license-url]\n\n<!-- PROJECT LOGO -->\n<br />\n<p align="center">\n  <a href="https://github.com/paypi/paypi-python">\n    <img src="images/logo.png" alt="Logo" height="80">\n  </a>\n\n  <h3 align="center">PayPI Python Client</h3>\n\n  <p align="center">\n    Sell your API, today.\n    <br />\n    <a href="https://partner.paypi.dev/"><strong>Explore the docs »</strong></a>\n    <br />\n    <br />\n    <a href="https://paypi.dev/">Homepage</a>\n    ·\n    <a href="https://github.com/paypi/paypi-python/issues">Report Bug</a>\n    ·\n    <a href="https://github.com/paypi/paypi-python/issues">Request Feature</a>\n  </p>\n</p>\n\n<!-- TABLE OF CONTENTS -->\n\n## Table of Contents\n\n- [About the Project](#about-the-project)\n- [Getting Started](#getting-started)\n  - [Prerequisites](#prerequisites)\n  - [Installation](#installation)\n- [Usage](#usage)\n- [Roadmap](#roadmap)\n- [Contributing](#contributing)\n- [License](#license)\n- [Contact](#contact)\n- [Acknowledgements](#acknowledgements)\n\n<!-- ABOUT THE PROJECT -->\n\n## About The Project\n\n[![PayPI Screenshot][product-screenshot]](https://paypi.dev)\n\nPayPI makes API creators\' lives easier by handling API keys, user accounts, payments and more.\nAPI users have one account to access all APIs using PayPI.\n\nWe worry about API authentication and payments so you can focus on making awesome APIs! This library enables you to interact with PayPI from a Python project.\n\n<!-- GETTING STARTED -->\n\n## Getting Started\n\n> <a href="https://partner.paypi.dev/"><strong>See full documentation here</strong></a>\n\nInstall `paypi` from PyPI:\n\n```sh\npip install paypi\n# or\npython -m pip install paypi\n```\n\nThen import it, create an instance with your private key and use it to authenticate and make charges against users:\n\n```python\nfrom paypi import PayPI\n\npaypi = PayPI("<Your API Secret>")\n\n\n@app.route("/")\ndef hello():\n    user = paypi.authenticate("<Users Subscription Secret>")\n\n    # do some work...\n\n    user.make_charge("<Charge ID>")\n    # charge is now made...\n```\n\nIn an asynchronous environment you can also use the asynchronous API calls:\n\n```python\npaypi = PayPI("<Your API Secret>")\nuser = await paypi.authenticate_async("Users Subscription Secret")\nawait user.make_charge_async("<Charge ID>")\n```\n\n<!-- ROADMAP -->\n\n## Roadmap\n\nSee the [open issues](https://github.com/paypi/paypi-python/issues) for a list of proposed features (and known issues).\n\n<!-- CONTRIBUTING -->\n\n## Contributing\n\nAll contributions are welcome. Please follow this workflow:\n\n1. Fork the Project\n2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)\n3. Commit your Changes (`git commit -m \'Add some AmazingFeature\'`)\n4. Push to the Branch (`git push origin feature/AmazingFeature`)\n5. Open a Pull Request\n\n<!-- LICENSE -->\n\n## License\n\nAll rights reserved.\n\n<!-- CONTACT -->\n\n## Contact\n\nAlex - alex@paypi.dev  \nTom - tom@paypi.dev\n\nProject Link: [https://github.com/paypi/paypi-python](https://github.com/paypi/paypi-python)\n\n<!-- ACKNOWLEDGEMENTS -->\n\n## Acknowledgements\n\n- [Img Shields](https://shields.io)\n- [Choose an Open Source License](https://choosealicense.com)\n\n<!-- MARKDOWN LINKS & IMAGES -->\n<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->\n\n[contributors-shield]: https://img.shields.io/github/contributors/Paypi/paypi-python.svg?style=flat-square\n[contributors-url]: https://github.com/paypi/paypi-python/graphs/contributors\n[forks-shield]: https://img.shields.io/github/forks/Paypi/paypi-python.svg?style=flat-square\n[forks-url]: https://github.com/paypi/paypi-python/network/members\n[stars-shield]: https://img.shields.io/github/stars/Paypi/paypi-python.svg?style=flat-square\n[stars-url]: https://github.com/paypi/paypi-python/stargazers\n[issues-shield]: https://img.shields.io/github/issues/Paypi/paypi-python.svg?style=flat-square\n[issues-url]: https://github.com/paypi/paypi-python/issues\n[license-shield]: https://img.shields.io/github/license/Paypi/paypi-python.svg?style=flat-square\n[license-url]: https://github.com/paypi/paypi-python/blob/master/LICENSE\n[product-screenshot]: images/product.png\n',
    'author': 'PayPI',
    'author_email': 'hello@paypi.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://paypi.dev',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
