# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tablespoon']

package_data = \
{'': ['*'],
 'tablespoon': ['stan/mean.stan',
                'stan/mean.stan',
                'stan/mean.stan',
                'stan/naive.stan',
                'stan/naive.stan',
                'stan/naive.stan',
                'stan/snaive.stan',
                'stan/snaive.stan',
                'stan/snaive.stan']}

install_requires = \
['cmdstanpy>=0.9.77,<0.10.0',
 'numpy>=1.21.2,<2.0.0',
 'pandas>=1.3.2,<2.0.0',
 'pytest>=6.2.5,<7.0.0']

setup_kwargs = {
    'name': 'tablespoon',
    'version': '0.1.4',
    'description': 'Simple probabilistic time series benchmark models',
    'long_description': '<h1 align="center">tablespoon</h1>\n<p align="center"><b>T</b>ime-series <b>B</b>enchmarks methods that are <b>S</b>imple and <b>P</b>robabilistic</p>\n\n# Documentation and quick links\n\n* [Introduction](#introduction)\n* [Why Run Simple Methods](#why-run-simple-methods)\n* [Goals of this package](#goals-of-this-package)\n* [Non-Goals](#non-goals)\n* [Forecast Method Documentation](docs/FORECAST_METHODS.md)\n* [Installation](#installation)\n* [Quick Example](#quick-example)\n* [Recommended probabilistic forecasting packages](#recommended-probabilistic-forecasting-packages)\n* [Learn more about forecasting](#learn-more-about-forecasting)\n\n# Introduction\n\nMany methods exist for probabilistic forecasting. If you are looking for\nimpressive probabilistic forecasting package see the list of recommendation at\nthe bottom of this README. It is expected that this package may be used as a\ncompliment to what is already out there.  \n\nThis package does **not** introduce\nnew forecasting models. Instead, this package focuses on making existing simple\nforecasting methods accessible.\n\nTo often we see that forecast method go in\nproduction without a naive method to accompany it. In our eyes we see that this\nis a missed opportunity. \n\n# Why Run Simple Methods\n\nThis package does **not** introduce new forecasting models. It is fantastically ordinary.\nWe have found, by experience, many good uses for the methods in this package.\n\n1. **Naive May Be Good Enough**: Some applications do not need anything more\n   impressive than a simple forecasting method.\n2. **Get A Denominator for Relative Metrics**: Though naive methods can usually\n   be beat it is good to know the relative improvement over the benchmark. This\n   can allow a forecasting team to market their alternative forecast when the\n   \'skill score\' is impressive.\n3. **Easy to productionize and expectations**: Get a sense for how good is good\n   enough. In many applications a forecast team is asked to forecast, but\n   stakeholders provide no line-in-the-sand for when the forecasting work needs\n   to stop. One reasonable approach is to run the benchmarks found in this\n   package in beat the best performing benchmark by a margin that is\n   statistically significant.\n4. **Resistance in Production - Why not have many models?**: Sometimes, despite\n   out best efforts our production model does something unexpected. In this\n   case it is nice to have a simple backup that is cheap to generate and good\n   enough to fall back on. In this way a production forecast pipeline gains\n   strength from a diversity of models.\n5. **Easy Uncertainty Quantification**: More and more we see that application\n   are not about forecast accuracy, but instead about forecasting uncertainty.\n   Capturing the full distribution helps firms set "service levels" aka\n   percentiles of the distribution for which they are prepared to serve. Even\n   if you have the worlds most accurate unbiased forecast the median point is\n   an underforecast half the time. For this reason it is best to provide a\n   distribution of simulated future values and the firm may decide for\n   themselves what risks they are or are not willing to take.\n\n# Goals of this package\n\n1. **Simplicity**: Not just in the forecasts themselves, but also from the\n   users perspective.\n2. **Accessability**: Because of how important we feel simple forecasting\n   methods are we want as many front end binding as possible to expose these\n   methods to the largest audience possible. We eventually have binding in\n   `Shell`,`Julia`,`R`, and `Python`.\n3. **Stability**: We want this package to feel rock solid. For this to happen\n   we keep the feature set relatively small. We believe that after the initial \n   development of this package we should spend out time maintaining the code as\n   oppose to thinking of new features.\n4. **Distributional Forecasts**: Quantification of uncertainty is the name of\n   the game.\n5. **Documentation**: It should be very clear exactly how forecasts are getting\n   generated. We document the parameterization of the models to make this as\n   obvious and uninteresting as possible.\n\n# Non-Goals\n\n1. **Circut Melting Speeds**: Not to say this is a slow package. In fact, all\n   models do get compiled.\n2. **New Forecast Models**: Again, this is out of scope. If you are\n   looking for recommendations please see the bottom of the page.\n\n# Installation\n\n### Python\n\n```\npip3 install tablespoon\n```\n\n# Quick Example\n\nWe show a quick example below. For more examples see [EXAMPLES.md](docs/EXAMPLES.md)\n\n```python\nimport numpy as np\nimport pandas as pd\nimport tablespoon as tbsp\nfrom cmdstanpy import install_cmdstan\n\n\n# If this is your first time installing cmdstanpy\ninstall_cmdstan()\n\n# pull and clean data\n# columns must have the columns "ds" and "y"\ndf = (\n    pd.read_csv("https://storage.googleapis.com/data_xvzf/m5_state_sales.csv")\n    .query("state_id == \'CA\'")\n    .rename(columns={"date": "ds", "sales": "y"})\n    .assign(y=lambda df: np.log(df.y))\n)\n\n# Snaive model\nsn = tbsp.Snaive()\ndf_sn = sn.predict(df, horizon=10)\nprint(df_sn.head())\n\n# Complete Data is Required: Models Error when time series is missing dates \nn = tbsp.Naive()\ndf_missing = df.drop([3])\ndf_n = n.predict(df_missing, horizon=10)\nprint(df_n.head())\n\n```\n\n# Recommended probabilistic forecasting packages\n\nThere are many packages that can compliment `tablespoon`\n\n[forecast](https://github.com/robjhyndman/forecast): The king of forecasting\npackages. Rob Hyndman is a professor of forecasting and has served as editor of\nthe journal "International Journal of Forecasting". If you are new to\nforecasting please read his free ebook [fpp3](https://otexts.com/fpp3/).\n\n[prophet](https://facebook.github.io/prophet/): A very capable and reliable\nforecasting package. I have never seen a bad forecast come out of prophet.\n\n[gluonts](https://ts.gluon.ai/). If you are itching to use neural nets for\nforecasting this is a good one to pick.\n\n# Learn more about forecasting\n\n1. Read [fpp3](https://otexts.com/fpp3/)\n2. Join the [International Institute of Forecasting](https://forecasters.org/)\n   and read their publications.\n\n',
    'author': 'Alex Hallam',
    'author_email': 'alexhallam6.28@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/well-made-spoon/tablespoon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
