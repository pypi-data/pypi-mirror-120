# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redisgraph']

package_data = \
{'': ['*']}

install_requires = \
['hiredis>=2.0.0,<3.0.0', 'prettytable>=2.1.0,<3.0.0', 'redis>=3.5.3,<4.0.0']

setup_kwargs = {
    'name': 'redisgraph',
    'version': '2.4.1',
    'description': 'RedisGraph Python Client',
    'long_description': '[![license](https://img.shields.io/github/license/RedisGraph/redisgraph-py.svg)](https://github.com/RedisGraph/redisgraph-py)\n[![CircleCI](https://circleci.com/gh/RedisGraph/redisgraph-py/tree/master.svg?style=svg)](https://circleci.com/gh/RedisGraph/redisgraph-py/tree/master)\n[![PyPI version](https://badge.fury.io/py/redisgraph.svg)](https://badge.fury.io/py/redisgraph)\n[![GitHub issues](https://img.shields.io/github/release/RedisGraph/redisgraph-py.svg)](https://github.com/RedisGraph/redisgraph-py/releases/latest)\n[![Codecov](https://codecov.io/gh/RedisGraph/redisgraph-py/branch/master/graph/badge.svg)](https://codecov.io/gh/RedisGraph/redisgraph-py)\n[![Known Vulnerabilities](https://snyk.io/test/github/RedisGraph/redisgraph-py/badge.svg?targetFile=pyproject.toml)](https://snyk.io/test/github/RedisGraph/redisgraph-py?targetFile=pyproject.toml)\n[![Total alerts](https://img.shields.io/lgtm/alerts/g/RedisGraph/redisgraph-py.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/RedisGraph/redisgraph-py/alerts/)\n\n# redisgraph-py\n[![Forum](https://img.shields.io/badge/Forum-RedisGraph-blue)](https://forum.redislabs.com/c/modules/redisgraph)\n[![Discord](https://img.shields.io/discord/697882427875393627?style=flat-square)](https://discord.gg/gWBRT6P)\n\nRedisGraph python client\n\n\n## Example: Using the Python Client\n\n```python\nimport redis\nfrom redisgraph import Node, Edge, Graph, Path\n\nr = redis.Redis(host=\'localhost\', port=6379)\n\nredis_graph = Graph(\'social\', r)\n\njohn = Node(label=\'person\', properties={\'name\': \'John Doe\', \'age\': 33, \'gender\': \'male\', \'status\': \'single\'})\nredis_graph.add_node(john)\n\njapan = Node(label=\'country\', properties={\'name\': \'Japan\'})\nredis_graph.add_node(japan)\n\nedge = Edge(john, \'visited\', japan, properties={\'purpose\': \'pleasure\'})\nredis_graph.add_edge(edge)\n\nredis_graph.commit()\n\nquery = """MATCH (p:person)-[v:visited {purpose:"pleasure"}]->(c:country)\n\t\t   RETURN p.name, p.age, v.purpose, c.name"""\n\nresult = redis_graph.query(query)\n\n# Print resultset\nresult.pretty_print()\n\n# Use parameters\nparams = {\'purpose\':"pleasure"}\nquery = """MATCH (p:person)-[v:visited {purpose:$purpose}]->(c:country)\n\t\t   RETURN p.name, p.age, v.purpose, c.name"""\n\nresult = redis_graph.query(query, params)\n\n# Print resultset\nresult.pretty_print()\n\n# Use query timeout to raise an exception if the query takes over 10 milliseconds\nresult = redis_graph.query(query, params, timeout=10)\n\n# Iterate through resultset\nfor record in result.result_set:\n\tperson_name = record[0]\n\tperson_age = record[1]\n\tvisit_purpose = record[2]\n\tcountry_name = record[3]\n\nquery = """MATCH p = (:person)-[:visited {purpose:"pleasure"}]->(:country) RETURN p"""\n\nresult = redis_graph.query(query)\n\n# Iterate through resultset\nfor record in result.result_set:\n    path = record[0]\n    print(path)\n\n\n# All done, remove graph.\nredis_graph.delete()\n```\n\n## Installing\n\n### Install official release\n\n```\npip install redisgraph\n```\n### Install latest release (Aligned with RedisGraph master)\n\n```\npip install git+https://github.com/RedisGraph/redisgraph-py.git@master\n```\n\n### Install for development in env\n\n1. Create a virtualenv to manage your python dependencies, and ensure it\'s active.\n   ```virtualenv -v venv; source venv/bin/activate```\n\n2. Install [pypoetry](https://python-poetry.org/) to manage your dependencies.\n   ```pip install poetry```\n\n3. Install dependencies.\n   ```poetry install```\n\n[tox](https://tox.readthedocs.io/en/latest/) runs all code linters as its default target.\n',
    'author': 'RedisLabs',
    'author_email': 'oss@redislabs.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
