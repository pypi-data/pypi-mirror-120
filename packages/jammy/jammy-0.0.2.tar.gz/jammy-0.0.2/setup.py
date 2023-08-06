# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jammy',
 'jammy.cli',
 'jammy.collections',
 'jammy.comm',
 'jammy.event',
 'jammy.image',
 'jammy.io',
 'jammy.logging',
 'jammy.random',
 'jammy.storage.kv',
 'jammy.utils',
 'jamnp',
 'jamtorch',
 'jamtorch.cuda',
 'jamtorch.data',
 'jamtorch.ddp',
 'jamtorch.distributions',
 'jamtorch.io',
 'jamtorch.logging',
 'jamtorch.nn',
 'jamtorch.prototype',
 'jamtorch.trainer',
 'jamtorch.utils',
 'jamviz',
 'jamviz.plt',
 'jamweb',
 'jamweb.session',
 'jamweb.web']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.17,<4.0.0',
 'attrs>=20.3.0,<21.0.0',
 'einops>=0.3.0,<0.4.0',
 'gpustat>=0.6.0,<0.7.0',
 'h5py>=3.4.0,<4.0.0',
 'hydra-core>=1.1.0,<2.0.0',
 'ipdb>=0.13.8,<0.14.0',
 'lmdb>=1.2.1,<2.0.0',
 'loguru>=0.5.3,<0.6.0',
 'matplotlib>=3.3.0,<4.0.0',
 'numpy>=1.20.3,<2.0.0',
 'python-memcached>=1.59,<2.0',
 'scipy>=1.6.3,<2.0.0',
 'torch>=1.9.0,<2.0.0',
 'torchvision>=0.10.0,<0.11.0',
 'tornado>=6.1,<7.0',
 'tqdm>=4.11.0,<5.0.0',
 'wandb>=0.10.31,<0.11.0']

setup_kwargs = {
    'name': 'jammy',
    'version': '0.0.2',
    'description': 'Personal ToolBox',
    'long_description': '# Jammy (Jam)\n\n**Jammy** is a personal toolkit.\n\n\n### Etymology\n* The naming is inspired from [Jyutping](https://en.wikipedia.org/wiki/Jyutping) of [Qin](https://en.wiktionary.org/wiki/%E6%AC%BD).\n\n## MICS\n\n* The package and framework are inspired from [Jacinle](https://github.com/vacancy/Jacinle) by [vacancy](https://github.com/vacancy), from which I learn and take utility functions shamelessly.\n',
    'author': 'Qin',
    'author_email': 'qsh.zh27@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
