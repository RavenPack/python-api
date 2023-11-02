from setuptools import find_packages, setup

from ravenpackapi import __version__

with open("README.rst") as readme_file:
    readme = readme_file.read()

setup(
    name="ravenpackapi",
    version=__version__,
    packages=find_packages(include=["ravenpackapi"]),
    package_data={"ravenpackapi": ["ravenpackapi/*"]},
    include_package_data=True,
    url="https://github.com/RavenPack/python-api",
    license="MIT",
    long_description=readme,
    author="RavenPack",
    author_email="dataservices@ravenpack.com",
    description="RavenPack API - Python client",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 5 - Production/Stable",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: System :: Software Distribution",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: MIT License",
    ],
    keywords="python analytics api rest news data",
    install_requires=["requests[security]", "python-dateutil", "six", "retry"],
)
