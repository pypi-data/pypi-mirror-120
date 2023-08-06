# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['df2img']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.3,<4.0.0', 'pandas>=1.3.3,<2.0.0']

setup_kwargs = {
    'name': 'df2img',
    'version': '0.1.0',
    'description': 'Save a Pandas DataFrame as image',
    'long_description': '########################################\ndf2img: Save a Pandas DataFrame as image\n########################################\n\nWhat is it all about?\n*********************\n| Have you ever tried to save a ``pd.DataFrame`` into an image file? This is not a straightforward process at all. Unfortunately, ``pandas`` itself doesn\'t provide this functionality out of the box.\n| **df2img** tries to fill the gap. It is a Python library that greatly simplifies the process of saving a ``pd.DataFrame`` into an image file (e.g. ``png`` or ``jpg``).\n\nDependencies\n************\n**df2img** has a limited number of dependencies, namely\n\n- ``pandas``\n- ``matplotlib``\n\nQuickstart\n**********\n\nYou can install the package via ``pip``.\n\n.. code:: python\n\n    pip install df2img\n\nLet\'s create a simple ``pd.DataFrame`` with some dummy data:\n\n.. code:: python\n\n    import pandas as pd\n\n    from df2img import df2img\n\n    df = pd.DataFrame(\n        data=dict(\n            float_col=[1.4, float("NaN"), 250, 24.65],\n            str_col=("string1", "string2", float("NaN"), "string4"),\n        ),\n        index=["row1", "row2", "row3", "row4"],\n    )\n\n.. code::\n\n          float_col  str_col\n    row1       1.40  string1\n    row2        NaN  string2\n    row3     250.00      NaN\n    row4      24.65  string4\n\nBasics\n------\n\nSaving ``df`` into a png-file is now a one-liner.\n\n.. code:: python\n\n    df2img(df, file="plot1.png")\n\n.. image:: https://github.com/andreas-vester/df2img/blob/main/docs/plot1.png?raw=true\n    :alt: plot1.png\n\nFormatting\n----------\n\nSetting the header row in a different color:\n\n.. code:: python\n\n    df2img(\n        df,\n        file="plot2.png",\n        header_color="white",\n        header_bgcolor="darkred",\n    )\n\n.. image:: https://github.com/andreas-vester/df2img/blob/main/docs/plot2.png?raw=true\n    :alt: plot2.png\n\n\n| You can alternate row colors for better readability. Using HEX colors is also possible:\n\n.. code:: python\n\n    df2img(\n        df,\n        file="plot3.png",\n        header_color="white",\n        header_bgcolor="darkred",\n        row_bgcolors=["#d7d8d6", "#ffffff"],\n    )\n\n.. image:: https://github.com/andreas-vester/df2img/blob/main/docs/plot3.png?raw=true\n    :alt: plot3.png\n\n\n| Setting the title, font size, column width, and row height:\n\n.. code:: python\n\n    df2img(\n        df,\n        file="plot4.png",\n        title="This is a title",\n        title_loc="left",\n        header_color="white",\n        header_bgcolor="darkred",\n        row_bgcolors=["#d7d8d6", "#ffffff"],\n        font_size=10.0,\n        col_width=1.5,\n        row_height=0.3\n    )\n\n.. image:: https://github.com/andreas-vester/df2img/blob/main/docs/plot4.png?raw=true\n    :alt: plot4.png\n\nContributing to df2img\n**********************\nAll bug reports and bug fixes, improvements to the documentation, or general ideas are welcome. Simply open an `issue <https://github.com/andreas-vester/df2img/issues>`_.\n\n',
    'author': 'Andreas Vester',
    'author_email': 'andreas@vester-online.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andreas-vester/df2img',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
