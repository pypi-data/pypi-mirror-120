from setuptools import setup

name = "types-backports_abc"
description = "Typing stubs for backports_abc"
long_description = '''
## Typing stubs for backports_abc

This is a PEP 561 type stub package for the `backports_abc` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `backports_abc`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/backports_abc. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `caa642dd3b10bb20179d81cb2821f25aa2695396`.
'''.lstrip()

setup(name=name,
      version="0.5.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['backports_abc-stubs'],
      package_data={'backports_abc-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
