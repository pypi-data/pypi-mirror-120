# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['basesqlmodel']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.68.1,<0.69.0', 'sqlmodel>=0.0.4,<0.0.5']

setup_kwargs = {
    'name': 'basesqlmodel',
    'version': '0.1.0',
    'description': 'A very simple CRUD class for SQLModel! :sparkles:',
    'long_description': '<h1 align="center">\n    <strong>basesqlmodel</strong>\n</h1>\n<p align="center">\n    <a href="https://github.com/Kludex/basesqlmodel" target="_blank">\n        <img src="https://img.shields.io/github/last-commit/Kludex/basesqlmodel" alt="Latest Commit">\n    </a>\n        <img src="https://img.shields.io/github/workflow/status/Kludex/basesqlmodel/Test">\n        <img src="https://img.shields.io/codecov/c/github/Kludex/basesqlmodel">\n    <br />\n    <a href="https://pypi.org/project/basesqlmodel" target="_blank">\n        <img src="https://img.shields.io/pypi/v/basesqlmodel" alt="Package version">\n    </a>\n    <img src="https://img.shields.io/pypi/pyversions/basesqlmodel">\n    <img src="https://img.shields.io/github/license/Kludex/basesqlmodel">\n</p>\n\nA very simple CRUD class for SQLModel! :sparkles:\n\n## Installation\n\n``` bash\npip install basesqlmodel\n```\n\n## Usage\n\n```python\nimport asyncio\n\nfrom sqlalchemy.ext.asyncio import AsyncSession, create_async_engine\nfrom sqlalchemy.orm import sessionmaker\nfrom sqlmodel import Field\n\nfrom basesqlmodel import Base\n\nengine = create_async_engine("sqlite+aiosqlite:///:memory:")\nSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)\n\n\nclass Potato(Base, table=True):\n    id: int = Field(primary_key=True)\n    name: str\n\n\nasync def main():\n    # Create tables\n    async with engine.begin() as conn:\n        await conn.run_sync(Base.metadata.create_all)\n\n    # Interact with the Potato table\n    async with SessionLocal() as session:\n        obj = await Potato.create(session, name="Potato")\n        print(f"Potato created: {repr(obj)}")\n\n        obj = await Potato.get(session, name="Potato")\n        print(f"Potato retrieved: {repr(obj)}")\n\n        await obj.update(session, name="Fake Potato")\n        print(f"Potato updated: {repr(obj)}")\n\n        await Potato.delete(session, name="Fake Potato")\n        print(f"Potato deleted: {repr(obj)}")\n\n        objs = await Potato.get_multi(session)\n        print(f"Confirm that the database is empty: {objs}")\n\n\nasyncio.run(main())\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Marcelo Trylesinski',
    'author_email': 'marcelotryle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kludex/basesqlmodel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
