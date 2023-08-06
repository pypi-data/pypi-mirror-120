# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hdate']

package_data = \
{'': ['*']}

install_requires = \
['pytz>=2020.0']

extras_require = \
{':python_version >= "2.7" and python_version < "2.8"': ['enum34>=1.1.10,<2.0.0'],
 ':python_version >= "3.6" and python_version < "4.0"': ['astral>=2.2,<3.0']}

setup_kwargs = {
    'name': 'hdate',
    'version': '0.10.4',
    'description': 'Jewish/Hebrew date and Zmanim in native Python 2.7/3.x',
    'long_description': '***********\npy-libhdate\n***********\n\nJewish/Hebrew date and Zmanim in native python 2.7/3.x\n\nOriginally ported from libhdate, see http://libhdate.sourceforge.net/ for more details (including license)\n\n===========\n\nInstallation using pip:\n#######################\n\n.. code :: shell\n\n    $ pip install hdate\n\n===========\n\nExamples:\n#########\n\nbase code to provide times of the day in hebrew:\n\n.. code :: python\n\n    >>> import hdate\n    >>> import datetime\n    >>> c = hdate.Location("פתח תקוה", 32.08707, 34.88747, "Asia/Jerusalem", 54)\n    >>> z = hdate.Zmanim(date=datetime.date(2016, 4, 18), location=c, hebrew=True)\n    >>> print(z)\n\n::\n\n    עלות השחר - 04:52:00\n    זמן טלית ותפילין - 05:18:00\n    הנץ החמה - 06:08:00\n    סוף זמן ק"ש מג"א - 08:46:00\n    סוף זמן ק"ש גר"א - 09:23:00\n    סוף זמן תפילה מג"א - 10:04:00\n    סוף זמן תפילה גר"א - 10:28:00\n    חצות היום - 12:40:00\n    מנחה גדולה - 13:10:30\n    מנחה קטנה - 16:25:30\n    פלג המנחה - 17:50:45\n    שקיעה - 19:12:00\n    צאת הכוכבים - 19:38:00\n    חצות הלילה - 00:40:00\n\nand in english:\n\n.. code :: python\n\n    >>> z = hdate.Zmanim(date=datetime.date(2016, 4, 18), location=c, hebrew=False)\n    >>> print(z)\n\n::\n\n    Alot HaShachar - 04:52:00\n    Talit & Tefilin\'s time - 05:18:00\n    Sunrise - 06:08:00\n    Shema EOT MG"A - 08:46:00\n    Shema EOT GR"A - 09:23:00\n    Tefila EOT MG"A - 10:04:40\n    Tefila EOT GR"A - 10:28:00\n    Midday - 12:40:00\n    Big Mincha - 13:10:30\n    Small Mincha - 16:25:30\n    Plag Mincha - 17:50:45\n    Sunset - 19:12:00\n    First stars - 19:38:00\n    Midnight - 00:40:00\n\n===========\n\nto provide the full hebrew date:\n\n.. code :: python\n\n    >>> h = hdate.HDate(datetime.date(2016, 4, 26), hebrew=True)\n    >>> print(h)\n\n::\n\n    יום שלישי י"ח בניסן התשע"ו ג\' בעומר חול המועד פסח\n\nand in english:\n\n.. code :: python\n\n    >>> h = hdate.HDate(datetime.date(2016, 4, 18), hebrew=False)\n    >>> print(h)\n\n::\n\n    Monday 10 Nisan',
    'author': 'Royi Reshef',
    'author_email': 'roy.myapp@gmail.com',
    'maintainer': 'Tsvi Mostovicz',
    'maintainer_email': 'ttmost@gmail.com',
    'url': 'https://github.com/py-libhdate/py-libhdate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
