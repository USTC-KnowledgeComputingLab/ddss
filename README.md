# Distributed Deductive System Sorts

## Versioning

This project uses [setuptools-scm](https://github.com/pypa/setuptools_scm/) for automatic versioning from git tags. The version is dynamically determined during build time based on git tags and commits.

To create a new release:
```bash
git tag v0.0.17
git push origin v0.0.17
```

## Building

To build the package:
```bash
python -m pip install build
python -m build
```
