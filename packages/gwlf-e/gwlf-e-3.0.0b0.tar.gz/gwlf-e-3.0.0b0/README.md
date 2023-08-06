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

Then publish the wheel to PyPI using credentials from LastPass:

```console
$ 
```

Finally, finish the release:

```console
$ git flow release finish -p 0.1.0
```

## License

This project is licensed under the terms of the Apache 2.0 license.
