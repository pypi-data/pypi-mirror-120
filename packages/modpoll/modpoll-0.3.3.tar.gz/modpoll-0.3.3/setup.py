# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['modpoll']

package_data = \
{'': ['*']}

install_requires = \
['paho-mqtt>=1.5.1,<2.0.0', 'pymodbus>=2.5.2,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

entry_points = \
{'console_scripts': ['modpoll = modpoll:app']}

setup_kwargs = {
    'name': 'modpoll',
    'version': '0.3.3',
    'description': 'A command line tool to communicate with modbus devices',
    'long_description': '# ModPoll - A command line tool to communicate with modbus devices.\n\n[![pipeline status](https://gitlab.com/helloysd/modpoll/badges/master/pipeline.svg)](https://gitlab.com/helloysd/modpoll/-/commits/master)\n[![License](https://img.shields.io/pypi/l/modpoll)](https://gitlab.com/helloysd/modpoll/-/blob/master/LICENSE)\n[![Downloads](http://pepy.tech/badge/modpoll)](http://pepy.tech/project/modpoll)\n\n> Learn more about `modpoll` usage at [documentation](https://helloysd.gitlab.io/modpoll) site. \n\n## Motivation\n\nThe initial idea of creating this tool is to help myself debugging new devices during site survey. A site survey usually has limited time and space, working on-site also piles up some pressures. At that time, a portable swiss-knife toolkit is our best friend.\n\nThis program can be easily deployed to Raspberry Pi or similar embedded devices, continuously polling data from the connected modbus devices, you can choose to save data locally or forward uplink to a MQTT broker for easy debugging, the MQTT broker can be setup on the same Raspberry Pi or on the cloud. On the other hand, a smart phone (Android/Iphone) can be used to visualize collected data and control the devices remotely via the same MQTT broker. \n\nHowever, beside the above recommended setup, you can actually run this program on any PC or server with Python 3 support. One popular use case is to deploy the program onto a server and keep it running as a gateway to bridge between traditional industrial network and modern IoT edge/cloud infrustructure. \n\n> This program is designed as a standalone tool, if you are looing for a python library to communicate with modbus devices, please consider the following two great open source projects, [pymodbus](https://github.com/riptideio/pymodbus) or [minimalmodbus](https://github.com/pyhys/minimalmodbus)\n\n## Installation\n\nThis program is tested on python 3.6+.\n\n- Install with pip\n\n  The package is available in the Python Package Index, \n\n  ```bash\n  pip install modpoll\n  ```\n\n  Upgrade the tool via pip by the following command,\n\n  ```bash\n  pip install -U modpoll\n  ```\n\n## Basic Usage\n\n- Connect to Modbus TCP device\n\n  ```bash\n  modpoll --tcp modsim.topmaker.net --config examples/modsim.csv\n\n  ```\n\n- Connect to Modbus RTU device \n\n  ```bash\n  modpoll --rtu /dev/ttyUSB0 --rtu-baud 9600 --config examples/scpms6.csv\n\n  ```\n\n- Connect to Modbus TCP device and publish data to MQTT broker \n\n  ```bash\n  modpoll --tcp modsim.topmaker.net --config examples/modsim.csv --mqtt-host iot.eclipse.org\n\n  ```\n\n- Connect to Modbus TCP device and export data to local csv file\n\n  ```bash\n  modpoll --tcp modsim.topmaker.net --config examples/modsim.csv --export data.csv\n\n  ```\n\nPlease refer to [documentation](https://helloysd.gitlab.io/modpoll) site for more configures and examples.\n\n> Notes: some of the examples use our online modbus simulator at `modsim.topmaker.net` with standard `502` port, it helps user to quickly test the functions of `modpoll` tool. \n\n## Run in docker\n\nA docker image has been provided for user to directly run the program, \n\n  ```bash\n  docker run helloysd/modpoll modpoll --help\n  ```\n\nTo load the modbus register configure file, user may need to mount the volume to container, \nfor example, if the child folder `examples` contains the config file `modsim.csv`, we can mount it using the following command, \n\n  ```bash\n  docker run -v $(pwd)/examples:/app/examples helloysd/modpoll modpoll --tcp modsim.topmaker.net --config /app/examples/modsim.csv\n  ```\n\n## Credits\n\nThe implementation of this project is heavily inspired by the following two projects:\n- https://github.com/owagner/modbus2mqtt (MIT license)\n- https://github.com/mbs38/spicierModbus2mqtt (MIT license)\nThanks to Max Brueggemann and Oliver Wagner for their great work. \n\n## License\n\nMIT © [Ying Shaodong](helloysd@foxmail.com)\n',
    'author': 'Ying Shaodong',
    'author_email': 'helloysd@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://helloysd.gitlab.io/modpoll',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
