[![Gitlab Pipeline](https://gitlab.com/campfiresolutions/public/gnista.io-cli/badges/master/pipeline.svg)](https://gitlab.com/campfiresolutions/public/gnista.io-cli/-/pipelines)  [![Python Version](https://img.shields.io/pypi/pyversions/gnista-cli)](https://pypi.org/project/gnista-cli/)  [![PyPI version](https://img.shields.io/pypi/v/gnista-cli)](https://pypi.org/project/gnista-cli/)  [![License](https://img.shields.io/pypi/l/gnista-cli)](https://pypi.org/project/gnista-cli/)  [![Downloads](https://img.shields.io/pypi/dm/gnista-cli)](https://pypi.org/project/gnista-cli/) 

# gnista-cli
A cli for accessing gnista.io

# Installing
Install gnista-cli for all Users, remove `-a` if you want to install for your current user only
``` bash
pip install gnista-cli
python -m gnista_cli i -a
```

## Installing Visplore Python Library
In order to open Visplore directly from gnista.io you need to install Visplore's Python library as [documented](https://visplore.com/documentation/v2021a/dataimport/python.html) here under `Installation 2. Alternative: using pip to install it in your terminal`

# Opening Custom URL Protocol
The commandline is able to handle `hgnista` URLs and redirect them to a specific client.

In this example it opens the datapoint `45623780-6a9a-45e6-a522-650d4484a019`in `Visplore`
``` bash
python -m gnista_cli o hgnista://45623780-6a9a-45e6-a522-650d4484a019?client=visplore
```


## Links
**Website**
[![gnista.io](https://www.gnista.io/assets/images/gnista-logo-small.svg)](https://gnista.io)

**PyPi**
[![PyPi](https://pypi.org/static/images/logo-small.95de8436.svg)](https://pypi.org/project/gnista-cli/)

**GIT Repository**
[![Gitlab](https://about.gitlab.com/images/icons/logos/slp-logo.svg)](https://gitlab.com/campfiresolutions/public/gnista.io-cli)