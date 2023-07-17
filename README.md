[![PyPI version](https://badge.fury.io/py/template_pypi.svg)](https://badge.fury.io/py/template_pypi)
[![PyPi downloads](https://img.shields.io/pypi/dm/template_pypi)](https://img.shields.io/pypi/dm/template_pypi)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4284804.svg)](https://doi.org/10.5281/zenodo.4284804)
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/myorg/template_pypi/master?urlpath=lab)
[![Gitpod - Code Now](https://img.shields.io/badge/Gitpod-code%20now-blue.svg?longCache=true)](https://gitpod.io#https://github.com/myorg/template_pypi)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/myorg/template_pypi.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/myorg/template_pypi/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/myorg/template_pypi.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/myorg/template_pypi/context:python)

# template_pypi

## DELETE THIS LATER 
Download template_pypi and rename it

```
git clone git@github.com:kmedian/template_pypi.git mycoolpkg
cd mycoolpkg
bash rename.sh "myorg" "mycoolpkg" "Real Name"
```

Reinitialize the repo:

```
rm -rf .git
git init
git remote add origin git@github.com:myorg/mycoolpkg.git
```


## Usage

Table of Contents

* [Use Case 1](#use-case-1)


### Use Case 1


## Appendix

### Installation
The `template_pypi` [git repo](http://github.com/myorg/template_pypi) is available as [PyPi package](https://pypi.org/project/template_pypi)

```sh
pip install template_pypi
pip install git+ssh://git@github.com/myorg/template_pypi.git
```

### Install a virtual environment

```sh
python3.6 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
pip install -r requirements-dev.txt --no-cache-dir
pip install -r requirements-demo.txt --no-cache-dir
```

(If your git repo is stored in a folder with whitespaces, then don't use the subfolder `.venv`. Use an absolute path without whitespaces.)

### Python commands

* Jupyter for the examples: `jupyter lab`
* Check syntax: `flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')`
* Run Unit Tests: `PYTHONPATH=. pytest`

Publish

```sh
pandoc README.md --from markdown --to rst -s -o README.rst
python setup.py sdist 
twine upload -r pypi dist/*
```

### Clean up 

```sh
find . -type f -name "*.pyc" | xargs rm
find . -type d -name "__pycache__" | xargs rm -r
rm -r .pytest_cache
rm -r .venv
```


### Support
Please [open an issue](https://github.com/myorg/template_pypi/issues/new) for support.


### Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/myorg/template_pypi/compare/).
