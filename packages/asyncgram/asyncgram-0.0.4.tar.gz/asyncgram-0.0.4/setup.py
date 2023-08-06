# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['asyncgram']

package_data = \
{'': ['*']}

install_requires = \
['requests']

setup_kwargs = {
    'name': 'asyncgram',
    'version': '0.0.4',
    'description': 'A lightweight, asynchronous telegram logging client',
    'long_description': '# Telegram requirements\n\nTo be able to use this tool, you will require a Telegram bot token and a group chat ID. \n\n[Telegram bot token reference](https://core.telegram.org/bots#6-botfather)\n\n[Telegram group chat ID reference](https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id)\n\n# Installation\n\n```\npip install asyncgram\n```\n\n# Usage\n\nOnce you have your telegram bot token and group chat ID, and you\'ve install asyncgram, you are ready to get started. \n\n## Creating a client\n\n```\nfrom asyncgram import Asyncgram\n\n# replace XXX with your keys\nTG_BOT_TOKEN = "XXX"\nTG_GROUP_ID = "XXX"\n\nclient = Asyncgram(\n    tg_token = TG_BOT_TOKEN, \n    tg_group = TG_GROUP_ID\n)\n```\n\n## Logging messages\n\n```\nclient.start()\n\nmessages = [\n    \'Hello world\',\n    \'My name is codeman\',\n    \'My birthday was yesterday.\'\n]\n\nfor msg in messages: client.put(msg)\n\nclient.stop()\n```\n\nThis is a toy example to get you started. Recommended usage would be to put relevant messages from some form of a websocket connection such that it\'s logged in an asynchronous way.\n\n# Donations\n\nIf you liked this tool and would like to support me, kindly send your donations in ETH to 0xB08f9B316ddBCA4Dc5736153Cd63B8d9Bec46Bab',
    'author': 'sumermalhotra',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3,<4',
}


setup(**setup_kwargs)
