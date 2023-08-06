# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['requests_asserts']
install_requires = \
['requests>=2.22,<3.0', 'responses>=0.14.0,<0.15.0']

setup_kwargs = {
    'name': 'requests-asserts',
    'version': '0.1.3',
    'description': 'The library to help test your HTTP requests using unittests',
    'long_description': '# Requests-Asserts\n\n[![CircleCI](https://circleci.com/gh/ADR-007/requests-asserts.svg?style=svg)](https://circleci.com/gh/ADR-007/requests-asserts)\n[![Coverage Status](https://coveralls.io/repos/github/ADR-007/requests-asserts/badge.svg?branch=master)](https://coveralls.io/github/ADR-007/requests-asserts?branch=master)\n[![PyPI version](https://badge.fury.io/py/requests-asserts.svg)](https://badge.fury.io/py/requests-asserts)\n![PyPI - License](https://img.shields.io/pypi/l/requests-asserts)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/requests-asserts)\n![PyPI - Status](https://img.shields.io/pypi/status/requests-asserts)\n\nThe decorator and context manager to mock and verify HTTP requests made by `requests` library for `unittest`.\n\n## How to install\n\n```\npip install requests-asserts\n```\n\n## How to use\n\nMake a list of `RequestMock` elements that contain all information about the expected request and response.\nUse `RequestMock.assert_requests(request_mocks)` with the list as a decorator or context manager.\n\n### Example\n```py\nimport requests\nfrom unittests import TestCase \n\ndef get_likes_on_post(username, password, post_id):\n    access_token = requests.post(\n        \'http://my.site/login\',\n        json={\'username\': username, \'password\': password}\n    ).json()[\'access_token\']\n\n    likes = requests.get(\n        f\'http://my.site/posts/{post_id}\',\n        headers={\n            \'Accept\': \'application/json\', \n            \'Authorization\': f\'Bearer {access_token}\'\n        }\n    ).json()[\'likes\']\n\n    return likes\n\nclass TestGetLikesOnPost(TestCase):\n    @RequestMock.assert_requests([\n        RequestMock(\n            request_url=\'http://my.site/login\',\n            request_json={\'username\': \'the name\', \'password\': \'the password\'},\n            request_method=RequestMock.Method.POST,\n            response_json={"access_token": \'the-token\'}\n        ),\n        RequestMock(\n            request_url=\'http://my.site/posts/3\',\n            request_headers_contains={\'Authorization\': \'Bearer the-token\'},\n            response_json={\'name\': \'The cool story\', \'likes\': 42}\n        )\n    ])\n    def test_get_likes_on_post(self):\n        self.assertEqual(42, get_likes_on_post(\'the name\', \'the password\', 3))\n\n```\n',
    'author': 'Adrian Dankiv',
    'author_email': 'adr-007@ukr.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ADR-007/requests-asserts',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
