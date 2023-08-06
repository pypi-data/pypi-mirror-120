# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['galaxies_datasets',
 'galaxies_datasets.datasets',
 'galaxies_datasets.datasets.eagle',
 'galaxies_datasets.datasets.galaxy_zoo_2',
 'galaxies_datasets.datasets.galaxy_zoo_challenge',
 'galaxies_datasets.datasets.galaxy_zoo_decals',
 'galaxies_datasets.scripts',
 'galaxies_datasets.scripts.documentation',
 'galaxies_datasets.scripts.eagle']

package_data = \
{'': ['*'],
 'galaxies_datasets.datasets.eagle': ['dummy_data/RecalL0025N0752/27/*',
                                      'dummy_data/RecalL0025N0752/27/images/*',
                                      'dummy_data/RefL0025N0376/27/*',
                                      'dummy_data/RefL0025N0376/27/images/*',
                                      'dummy_data/RefL0025N0752/27/*',
                                      'dummy_data/RefL0025N0752/27/images/*',
                                      'dummy_data/RefL0100N1504/27/*',
                                      'dummy_data/RefL0100N1504/27/images/*'],
 'galaxies_datasets.datasets.galaxy_zoo_2': ['dummy_data/galaxy_zoo_2/*',
                                             'dummy_data/galaxy_zoo_2/images/*'],
 'galaxies_datasets.datasets.galaxy_zoo_challenge': ['dummy_data/galaxy_zoo_challenge/*',
                                                     'dummy_data/galaxy_zoo_challenge/images_test_rev1/*',
                                                     'dummy_data/galaxy_zoo_challenge/images_training_rev1/*'],
 'galaxies_datasets.datasets.galaxy_zoo_decals': ['dummy_data/galaxy_zoo_decals/*',
                                                  'dummy_data/galaxy_zoo_decals/gz_decals_dr5_png_part1/J004/*',
                                                  'dummy_data/galaxy_zoo_decals/gz_decals_dr5_png_part1/J005/*',
                                                  'dummy_data/galaxy_zoo_decals/gz_decals_dr5_png_part1/J022/*',
                                                  'dummy_data/galaxy_zoo_decals/gz_decals_dr5_png_part1/J074/*',
                                                  'dummy_data/galaxy_zoo_decals/gz_decals_dr5_png_part1/J075/*',
                                                  'dummy_data/galaxy_zoo_decals/gz_decals_dr5_png_part1/J081/*',
                                                  'dummy_data/galaxy_zoo_decals/gz_decals_dr5_png_part1/J084/*',
                                                  'dummy_data/galaxy_zoo_decals/gz_decals_dr5_png_part1/J085/*',
                                                  'dummy_data/galaxy_zoo_decals/gz_decals_dr5_png_part1/J092/*',
                                                  'dummy_data/galaxy_zoo_decals/gz_decals_dr5_png_part1/J100/*',
                                                  'dummy_data/galaxy_zoo_decals/gz_decals_dr5_png_part2/J112/*',
                                                  'dummy_data/galaxy_zoo_decals/gz_decals_dr5_png_part2/J125/*',
                                                  'dummy_data/galaxy_zoo_decals/gz_decals_dr5_png_part3/J124/*',
                                                  'dummy_data/galaxy_zoo_decals/gz_decals_dr5_png_part3/J133/*',
                                                  'dummy_data/galaxy_zoo_decals/gz_decals_dr5_png_part3/J134/*',
                                                  'dummy_data/galaxy_zoo_decals/gz_decals_dr5_png_part4/J151/*',
                                                  'dummy_data/galaxy_zoo_decals/gz_decals_dr5_png_part4/J152/*',
                                                  'dummy_data/galaxy_zoo_decals/gz_decals_dr5_png_part4/J164/*']}

install_requires = \
['eagleSqlTools>=2.0.0,<3.0.0',
 'pandas>=1.3.2,<2.0.0',
 'tensorflow-datasets>=4.4.0,<5.0.0',
 'tensorflow>=2.6.0,<3.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['galaxies_datasets = galaxies_datasets.__main__:app']}

setup_kwargs = {
    'name': 'galaxies-datasets',
    'version': '0.1.0',
    'description': 'Galaxies Datasets',
    'long_description': 'Galaxies Datasets\n=================\n\n|header|\n\n.. |header| image:: header.png\n   :alt: Galaxies Datasets\n\n|PyPI| |Status| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/galaxies_datasets.svg\n   :target: https://pypi.org/project/galaxies_datasets/\n   :alt: PyPI\n.. |Status| image:: https://img.shields.io/pypi/status/galaxies_datasets.svg\n   :target: https://pypi.org/project/galaxies_datasets/\n   :alt: Status\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/galaxies_datasets\n   :target: https://pypi.org/project/galaxies_datasets\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/galaxies_datasets\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/galaxies_datasets/latest.svg?label=Read%20the%20Docs\n   :target: https://galaxies_datasets.readthedocs.io/\n   :alt: Read the documentation at https://galaxies_datasets.readthedocs.io/\n.. |Tests| image:: https://github.com/lbignone/galaxies_datasets/workflows/Tests/badge.svg\n   :target: https://github.com/lbignone/galaxies_datasets/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/lbignone/galaxies_datasets/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/lbignone/galaxies_datasets\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\n*Galaxies Datasets* is a collection of ready-to-use extragalactic astronomy datasets\nfor use with TensorFlow, Jax, and other Machine Learning frameworks.\n\nIt follows the `tensorflow_datasets`_ framework, making it very easy to switch\nbetween different datasets. All datasets are exposed as `tf.data.Datasets`_, enabling\neasy-to-use and high-performance input pipelines.\n\n\nUsage\n-----\n\nLoading a dataset can be as easy as:\n\n.. code-block:: python\n\n    from galaxies_datasets import datasets\n    import tensorflow_datasets as tfds\n\n    # Construct a tf.data.Dataset\n    ds = tfds.load("galaxy_zoo_challenge", split="train")\n\n    # Build your input pipeline\n    ds = ds.shuffle(1000).batch(128).prefetch(10).take(5)\n\nIn the example above:\n\n.. code-block:: python\n\n    from galaxies_datasets import datasets\n\nregisters the collection of galactic datasets with the `tensorflow_datasets`_ package\nmaking them available through its API. And that is it! ...Almost.\n\nFor more details on tensorflow_datasets check out the `documentation`_.\n\nSome datasets require that you first manually download data. Check each dataset for\ninstructions.\n\n\nDatasets\n--------\n\nCurrently `available datasets`_ focus on galaxy morphology.\n\nThey include observational data from the `Galaxy zoo project`_:\n\n- galaxy_zoo_challenge\n- galaxy_zoo2\n- galaxy_zoo_decals\n\nAs well as mock galaxy images from the `EAGLE simulation`_:\n\n- eagle\n\n\nInstallation\n------------\n\nYou can install *Galaxies Datasets* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install galaxies_datasets\n\n\nScripts\n-------\n\n*Galaxies Datasets* provides some scripts to download and prepare data. The scripts\nare available through a command-line interface powered by `Typer`_.\n\nFor example, to download images and data from the EAGLE simulation you could simply do::\n\n    galaxies_datasets eagle download USER SIMULATION\n\nwhere USER is your username for the EAGLE public database and SIMULATION is the name\nof one of the EAGLE simulations.\n\nFor all available commands check the `Command-line Interface`_ reference, or run::\n\n    galaxies_datasets --help\n\nThe command-line interface also supports automatic completion in all operating\nsystems, in all the shells (Bash, Zsh, Fish, PowerShell), so that you can just hit\nTAB and get the available options or subcommands.\n\nTo install automatic completion in bash run::\n\n    galaxies_datasets --install-completion bash\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*Galaxies Datasets* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nDisclaimer\n----------\n\nThis is a utility library that downloads and prepares datasets. We do not host\nor distribute these datasets, vouch for their quality or fairness, or claim that you\nhave license to use the dataset. It is your responsibility to determine whether you\nhave permission to use the dataset under the dataset\'s license.\n\nIf you\'re a dataset owner and wish to update any part of it (description, citation,\netc.), or do not want your dataset to be included in this library, please get in\ntouch through a GitHub issue. Thanks for your contribution to the ML community!\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_\'s `Hypermodern Python Cookiecutter`_\ntemplate.\n\nIcons made by `Freepik <https://www.freepik.com>`_ from `www.flaticon.com\n<https://www.flaticon.com/>`_\n\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/lbignone/galaxies_datasets/issues\n.. _pip: https://pip.pypa.io/\n.. _tensorflow_datasets: https://www.tensorflow.org/datasets/\n.. _tf.data.Datasets: https://www.tensorflow.org/api_docs/python/tf/data/Dataset\n.. _documentation: https://www.tensorflow.org/datasets/overview\n.. _Galaxy zoo project: https://www.zooniverse.org/projects/zookeeper/galaxy-zoo/\n.. _EAGLE simulation: http://icc.dur.ac.uk/Eagle/\n.. _Typer: https://typer.tiangolo.com/\n.. github-only\n.. _available datasets: docs/datasets.md\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Command-line Interface: cli.rst\n.. _Usage: https://galaxies_datasets.readthedocs.io/en/latest/usage.html\n',
    'author': 'Lucas Bignone',
    'author_email': 'lbignone@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lbignone/galaxies_datasets',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
