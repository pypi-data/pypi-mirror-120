# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytest_fixture_maker']

package_data = \
{'': ['*']}

entry_points = \
{'pytest11': ['fixture_maker = pytest_fixture_maker.plugin']}

setup_kwargs = {
    'name': 'pytest-fixture-maker',
    'version': '0.2.0',
    'description': 'Pytest plugin to load fixtures from YAML files',
    'long_description': 'pytest-fixture-maker: Load fixture data from local YAML files.\n============\n\n[![Master](https://github.com/clayman083/pytest-fixture-maker/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/clayman083/pytest-fixture-maker/actions/workflows/main.yml)\n<!-- [![Coverage Status](https://coveralls.io/repos/github/clayman74/pytest-postgres/badge.svg?branch=master)](https://coveralls.io/github/clayman74/pytest-postgres?branch=master) -->\n[![PyPI version](https://badge.fury.io/py/pytest-fixture-maker.svg)](https://badge.fury.io/py/pytest-fixture-maker)\n[![PyPI](https://img.shields.io/pypi/pyversions/pytest-fixture-maker.svg)]()\n\npytest-fixture-maker is a plugin for pytest, which load fixtures data from local YAML files.\n\n\nExample file with fixtures:\n\n    # fixtures/test_fetch_by_key.yml\n\n    --- \n\n    test_fetch_by_key:\n      storage: \n        accounts:\n          - { key: 1, name: "Visa Classic" }\n          - { key: 2, name: "Visa Gold"}\n\n    test_success:\n      - id: First test case\n        account_key: 1\n        expected: { key: 1, name: "Visa Classic" }\n      - id: Second test case\n        account_key: 2\n        expected: { key: 2, name: "Visa Gold" }\n\n    test_missing:\n      - id: Try fetch missing account\n        account_key: 3\n        expected_exc: AccountNotFound\n\n\nExample conftest.py file:\n\n    # conftest.py\n\n    from typing import Any\n\n    import pytest\n\n    from tests.accounts import Account, AccountRepo, Storage\n\n\n    @pytest.fixture(scope="function")\n    def account(request) -> Account:\n        """Account entity."""\n        return Account(**request.param)\n\n\n    @pytest.fixture(scope="function")\n    def storage(request) -> Storage:\n        """Entity storage."""\n        storage = Storage()\n\n        if "accounts" in request.param:\n            accounts = [Account(**account) for account in request.param["accounts"]]\n            storage.accounts = AccountRepo(accounts=accounts)\n\n        return storage\n\n\n    @pytest.fixture(scope="function")\n    def expected(request) -> Any:\n        """Expected test case result."""\n        return request.param\n\n\nExample tests:\n\n    from typing import Type\n\n    import pytest\n\n    from tests.accounts import Account, AccountNotFound, Storage\n\n\n    @pytest.fixture\n    def account_key(request) -> int:\n        """Test account identifier."""\n        return request.param\n\n\n    @pytest.fixture\n    def expected(request) -> Account:\n        """Expected test case result."""\n        return Account(**request.param)\n\n\n    @pytest.mark.integration\n    def test_success(storage: Storage, account_key: int, expected: Account) -> None:\n        """Successful fetch account by key from storage."""\n        result = storage.accounts.fetch_by_key(account_key)\n\n        assert result == expected\n\n\n    @pytest.fixture\n    def expected_exc(request) -> Type[AccountNotFound]:\n        """Expected exception when account not found in storage."""\n        return AccountNotFound\n\n\n    @pytest.mark.integration\n    def test_missing(storage: Storage, account_key: int, expected_exc: Type[AccountNotFound]) -> None:\n        """Try to fetch missing account by key from storage."""\n        with pytest.raises(expected_exc):\n            storage.accounts.fetch_by_key(account_key)\n\n\nInstallation\n------------\n\nTo install pytest-fixture-maker, do:\n\n    (env) $ python3 -m pip install pytest-fixture-maker\n\n\nChangelog\n---------\n\n0.1.0 (2021-09-19)\n~~~~~~~~~~~~~~~~~~\nInitial release.\n',
    'author': 'Kirill Sumorokov',
    'author_email': 'sumorokov.k@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/clayman083/pytest-fixture-maker',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
