# Distributed Deductive System Sorts

## Versioning

This project uses [setuptools-scm](https://github.com/pypa/setuptools_scm/) for automatic versioning from git tags. The version is dynamically determined during build time based on git tags and commits.

### Version Format

- **Release version**: `0.0.16` (when built from a git tag like `v0.0.16`)
- **Development version**: `0.0.17.dev3+g6ff80e0` (when built from a commit after a tag)
  - `0.0.17`: Next version number
  - `dev3`: 3 commits after the last tag
  - `g6ff80e0`: Short git commit hash

### Creating a Release

To create a new release:
```bash
# Tag the release
git tag v0.0.17
git push origin v0.0.17

# Build the package
python -m pip install build
python -m build
```

The built package will automatically have version `0.0.17` from the tag.

## Building

To build the package:
```bash
python -m pip install build
python -m build
```
