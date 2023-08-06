# gwlf-e
Port of Generalized Watersheds Loading Functions - Enhanced (MapShed)

[![Build Status](https://travis-ci.org/WikiWatershed/gwlf-e.svg?branch=develop)](https://travis-ci.org/WikiWatershed/gwlf-e)

## Installation

Install using `pip`:

```bash
$ pip install gwlf-e
```

## Development

Ensure you have Python 3.9 and [pipenv](https://pipenv.pypa.io/en/latest/) available. Then run:

```bash
$ pipenv sync
```

### Testing

```bash
$ pipenv run nosetests
```

## Deployments

Create a new release using git flow:

```console
$ git flow release start 0.1.0
$ vim CHANGELOG.md
$ vim setup.py
$ git add CHANGELOG.md setup.py
$ git commit -m "0.1.0"
$ git flow release publish 0.1.0
```

Then create a wheel to publish to PyPI using [build](https://github.com/pypa/build):

```console
$ PYTHONPATH=. python -m build
```

This should create two files under `dist/`:

```console
$ ls -1 dist/
gwlf-e-3.0.0b0.tar.gz
gwlf_e-3.0.0b0-cp39-cp39-macosx_11_0_x86_64.whl
```

Then publish the wheel to PyPI using [twine](https://github.com/pypa/twine/) and credentials from LastPass:

```console
$ python -m twine check dist/*
Checking dist/gwlf_e-3.0.0b0-cp39-cp39-macosx_11_0_x86_64.whl: PASSED
Checking dist/gwlf-e-3.0.0b0.tar.gz: PASSED
```
```console
$ python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
Uploading distributions to https://test.pypi.org/legacy/
Enter your username: azavea
Enter your password:
Uploading gwlf_e-3.0.0b0-cp39-cp39-macosx_11_0_x86_64.whl
100%|
Uploading gwlf-e-3.0.0b0.tar.gz
100%|

View at:
https://test.pypi.org/project/gwlf-e/3.0.0b0/
```
```console

```

Finally, finish the release:

```console
$ git flow release finish -p 0.1.0
```

## License

This project is licensed under the terms of the Apache 2.0 license.
