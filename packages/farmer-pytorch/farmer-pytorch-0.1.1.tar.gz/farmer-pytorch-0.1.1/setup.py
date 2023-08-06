# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['farmer_pytorch',
 'farmer_pytorch.GetAnnotation',
 'farmer_pytorch.GetDataset',
 'farmer_pytorch.GetOptimization']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.3.2,<9.0.0', 'torch>=1.9.1,<2.0.0']

setup_kwargs = {
    'name': 'farmer-pytorch',
    'version': '0.1.1',
    'description': 'deep learning tools: easy to run, easy to customize',
    'long_description': '# Pytorch segmentation\n\n```bash\ndocker build -t pyroch_seg:latest .\n\ndocker run \\\n    --gpus all \\\n    -itd \\\n    --ipc=host \\\n    --shm-size=24g \\\n    -v /mnt:/mnt \\\n    --name cowboy \\\n    pyroch_seg:latest\n```\n',
    'author': 'aiorhiroki',
    'author_email': '1234defgsigeru@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aiorhiroki/farmer.pytorch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
