# earthdata
### A NASA CMR/EDL client library

<p align="center">
    <em>A summary phrase to catch attention!</em>
</p>

<p align="center">
<a href="https://github.com/betolink/earthdata/actions?query=workflow%3ATest" target="_blank">
    <img src="https://github.com/betolink/earthdata/workflows/Test/badge.svg" alt="Test">
</a>
<a href="https://github.com/betolink/earthdata/actions?query=workflow%3APublish" target="_blank">
    <img src="https://github.com/betolink/earthdata/workflows/Publish/badge.svg" alt="Publish">
</a>
<a href="https://dependabot.com/" target="_blank">
    <img src="https://flat.badgen.net/dependabot/betolink/earthdata?icon=dependabot" alt="Dependabot Enabled">
</a>
<a href="https://codecov.io/gh/betolink/earthdata" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/betolink/earthdata?color=%2334D058" alt="Coverage">
</a>
<a href="https://pypi.org/project/earthdata" target="_blank">
    <img src="https://img.shields.io/pypi/v/earthdata?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/earthdata/" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/earthdata.svg" alt="Python Versions">
</a>


## Overview


## Installing earthdata

Install the latest release:

```bash
pip install earthdata
```

Or you can clone `earthdata` and get started locally

```bash

# ensure you have Poetry installed
pip install --user poetry

# install all dependencies (including dev)
poetry install

# test

poetry run pytest

# develop!

```

## Example Usage

```python
from earthdata import Auth, DataGranules, DataCollections, Accessor

auth = Auth() # if we want to access NASA DATA in the cloud

collections = DataCollections(auth).keyword('MODIS').get(10)
collections

granules = DataGranules(auth).concept_id('C1711961296-LPCLOUD').bounding_box(-10,20,10,50).get(5)
granules

# We provide some convenience functions for each result
data_links = [granule.data_links() for granule in granules]
data_links

# The Acessor class allows to get the granules from on-prem locations with get()
# if you're in a AWS instance (us-west-2) you can use open() to get a fileset!
# NOTE: Some datasets require users to accept a Licence Agreement before accessing them
access = Accessor(auth)

# This works with both, on-prem or cloud based collections**
access.get(granules[0:10], './data')

# If we are running in us-west-2 we can use open !!
fileset = accessor.open(granules[0:10])

xarray.open_mfdataset(fileset, combine='by_coords')
```

Only **Python 3.7+** is supported as required by the black, pydantic packages


## Contributing Guide

Welcome! 😊👋

> Please see the [Contributing Guide](CONTRIBUTING.md).
