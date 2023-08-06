# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whill']

package_data = \
{'': ['*']}

install_requires = \
['pyserial>=3.5,<4.0']

setup_kwargs = {
    'name': 'whill',
    'version': '1.2.0',
    'description': 'WHILL Model CR SDK for Python',
    'long_description': '# pywhill\npywhill is a WHILL Model CR SDK for Python. <br>\nWe also have [Model CR Technical Support repository](https://github.com/WHILL/Model_CR_Technical_Support) for current and potential Model CR users. <br>\nFor general questions and requests, please visit our [product page](https://whill.inc/jp/model-cr) .\n\n<img src="https://user-images.githubusercontent.com/2618822/45492944-89421c00-b7a8-11e8-9c92-22aa3f28f6e4.png" width=30%>\n\n\n## Requirements\n- WHILL **Model CR**  (Normal **Model C** does not support serial communication.)\n- Python3.6 or later\n- pySerial (https://github.com/pyserial/pyserial)\n\n## OS Support\n- Windows 10\n- MacOS X\n- Ubuntu 16.04\n- Ubuntu 18.04\n\n## Getting Started\nClone or download this repository at any place you want, or this package is avalable on [PyPI](https://pypi.org/project/whill/).\n\n```\npython3 -m pip install whill\n```\n\n## APIs\n\n### Initialize\n\n```python\nfrom whill import ComWHILL\n<your_obj_name> = ComWHILL(port=<Your COM Port>)\n```\nInitialize WHILL instance with SoftwareSerial.\n\n### Communication\n\n```python\n<your_obj_name>.start_data_stream(interval_msec=<update interval in millisecond>)\n```\nCommand WHILL to start reporting WHILL status.\n\n```python\n<your_obj_name>.refresh()\n```\nFetch serial interface and do internal process.\n\n\n```python\n<your_obj_name>.stop_data_stream()\n```\nCommand WHILL to stop report WHILL status.\n\n\n### Manipulation\n\n```python\n<your_obj_name>.set_joy_stick(front=<Integer -100~100>, side=<Integer -100~100>)\n```\nManipulate a WHILL via this command.\nBoth `front` and `side` are integer values with range -100 ~ 100.\n\n\n```python\n<your_obj_name>.send_power_on()\n<your_obj_name>.send_power_off()\n<your_obj_name>.set_power(power_state_command=<True/False>)\n\n```\nTurn on/off a WHILL. `power_state_command` is a bool with `True` to power WHILL on.\n\n```python\n<your_obj_name>.set_battery_voltage_output_mode(vbatt_on_off=<True/False>)\n```\nEnable/Disable power supply to the interface connector. `True` to enable power supply.\n\n\n### Sensors and Status\n\n### Accelerometer **(deprecated)**\nAccelerometer API has been disabled since v1.2.0.\n\n#### Gyro **(deprecated)**\nGyro API has been disabled since v1.2.0.\n\n#### Battery\n```python\n<your_obj_name>.battery\n```\nRemaining battery level[%] and consumpting current[mA].\n\n\n#### Motor State\n```python\n<your_obj_name>.left_motor\n<your_obj_name>.right_motor\n```\nMotors angle and speed. The angle range is -PI to +PI, Speed unit is km/h.\n**Note that the speed value is low-pass filterd.**\n\n#### Speed Mode\n```python\n<your_obj_name>.speed_mode_indicator\n```\nCurrent selected speed mode.\n\n### Callback\n```python\n<your_obj_name>.register_callback(event=<either \'data_set_0\' or \'data_set_1\', func=<your callback function>)\n```\nBy registering callback functions, You can hook at status is updated.\nSee Example: [cr_example3_callback.py](https://github.com/WHILL/pywhill/blob/master/example/cr_example3_callback.py)\n\n## License\nMIT License\n',
    'author': 'Seiya Shimizu',
    'author_email': 'seiya.shimizu@whill.inc',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://whill.inc/jp/model-cr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
