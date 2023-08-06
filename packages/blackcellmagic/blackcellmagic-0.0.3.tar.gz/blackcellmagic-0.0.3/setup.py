# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['blackcellmagic']
install_requires = \
['black>=21.9b0,<22.0', 'jupyter>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'blackcellmagic',
    'version': '0.0.3',
    'description': 'IPython magic command to format python code in cell using black.',
    'long_description': 'blackcellmagic\n==============\n\n|pypiv| |pyv| |Licence| |Downloads|\n\nIPython magic command to format python code in cell using `black`_.\n\nWhat is the magic command?\n--------------------------\n\n.. code:: python\n\n    %%black\n\nSetup\n-----\n\nUsing pip\n~~~~~~~~~\n\n.. code:: bash\n\n    pip install blackcellmagic\n\nDirectly from the repository\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n.. code:: bash\n\n    git clone https://github.com/csurfer/blackcellmagic.git\n    python blackcellmagic/setup.py install\n\nLoad Extension in IPython\n~~~~~~~~~~~~~~~~~~~~~~~~~\n\n.. code:: python\n\n    %load_ext blackcellmagic\n\nUsage\n-----\n\n.. code:: python\n\n    # To have it formatted to black default length 88 with string normalization.\n    %%black\n\n    # To have it formatted to a particular line length.\n    %%black -l 79\n    %%black --line-length 79\n\n    # To skip string normalization.\n    %%black -S\n    %%black --skip-string-normalization\n\nExtras\n------\n\nTobin Jones has been kind enough to develop a NPM package over blackcellmagic to format all cells at once which can be found `here`_.\n\n\nContributing\n------------\n\nBug Reports and Feature Requests\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nPlease use `issue tracker`_ for reporting bugs or feature requests.\n\nDevelopment\n~~~~~~~~~~~\n\nPull requests are most welcome.\n\nBuy the developer a cup of coffee!\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nIf you found the utility helpful you can buy me a cup of coffee using\n\n|Donate|\n\n\n.. _black: https://github.com/ambv/black\n\n.. _issue tracker: https://github.com/csurfer/blackcellmagic/issues\n\n.. |Donate| image:: https://www.paypalobjects.com/webstatic/en_US/i/btn/png/silver-pill-paypal-44px.png\n   :target: https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=3BSBW7D45C4YN&lc=US&currency_code=USD&bn=PP%2dDonationsBF%3abtn_donate_SM%2egif%3aNonHosted\n\n.. |Licence| image:: https://img.shields.io/badge/license-MIT-blue.svg\n   :target: https://raw.githubusercontent.com/csurfer/blackcellmagic/master/LICENSE\n\n.. |pypiv| image:: https://img.shields.io/pypi/v/py-heat-magic.svg\n   :target: https://pypi.python.org/pypi/blackcellmagic\n\n.. |pyv| image:: https://img.shields.io/pypi/pyversions/blackcellmagic.svg\n   :target: https://pypi.python.org/pypi/blackcellmagic\n\n.. |Downloads| image:: https://pepy.tech/badge/blackcellmagic\n   :target: https://pepy.tech/project/blackcellmagic\n\n.. _here: https://github.com/tobinjones/jupyterlab_formatblack\n',
    'author': 'csurfer',
    'author_email': 'sharma.vishwas88@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/csurfer/blackcellmagic',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
