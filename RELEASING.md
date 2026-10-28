# Releasing a new version

Releases are published by the [deploy pipeline](.github/workflows/deploy.yml) when a version tag is pushed. To release version `X.Y.Z`:

1. Set `__version__ = "X.Y.Z"` in [ravenpackapi/version.py](ravenpackapi/version.py).
2. Add a `## [vX.Y.Z] (YYYY-MM-DD)` section at the top of [CHANGELOG.md](CHANGELOG.md). Its content becomes the GitHub release notes, and the release fails without it. You can preview it with `.github/changelogtext.sh`.
3. Commit both files as "Bump version", push `master` and wait for the CI pipeline to pass.
4. Tag that commit and push the tag:

   ```bash
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```

The pipeline then checks that the tag matches the version in the code, builds the packages, uploads them to [PyPI](https://pypi.org/p/ravenpackapi) and Anaconda, and creates the [GitHub release](https://github.com/RavenPack/python-api/releases).
