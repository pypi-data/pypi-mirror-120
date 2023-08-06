# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['waybar_openweathermap']

package_data = \
{'': ['*']}

install_requires = \
['geopy>=2.2.0,<3.0.0']

entry_points = \
{'console_scripts': ['waybar-openweathermap = waybar_openweathermap:main']}

setup_kwargs = {
    'name': 'waybar-openweathermap',
    'version': '1.0.2',
    'description': 'Weather info widget for Waybar, from OpenWeatherMap.org',
    'long_description': 'Waybar weather plugin\n=====================\n\nThis plugin uses the [One Call API from OpenWeatherMap.org](https://openweathermap.org/api/one-call-api).\n\n## set your APIKEY and geo location in your shell\n\nIn your ~/.bashrc add the following definition and place your APIKEY in there\n\n    # waybar weather settings:\n    export WAYBAR_WEATHER_APIKEY="<YOUR OpenWeatherMap API KEY>"\n    export WAYBAR_WEATHER_LAT="44.43"\n    export WAYBAR_WEATHER_LON="26.02"\n    export WAYBAR_WEATHER_UNITS="metric"\n    export WAYBAR_WEATHER_EXCLUDE="minutely,hourly,daily"',
    'author': 'Maik Derstappen - Derico',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MrTango/waybar-openweathermap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
