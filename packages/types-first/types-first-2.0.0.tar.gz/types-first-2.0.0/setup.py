from setuptools import setup

name = "types-first"
description = "Typing stubs for first"
long_description = '''
## Typing stubs for first

This is a PEP 561 type stub package for the `first` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `first`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/first. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `caa642dd3b10bb20179d81cb2821f25aa2695396`.
'''.lstrip()

setup(name=name,
      version="2.0.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['first-stubs'],
      package_data={'first-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
