import sys
from setuptools import setup, find_packages

setup(name="meshcatmods",
    version="0.1.2",
    description="Forked version of meshcat-python for BCI Gym.",
    url="https://github.com/aplbrain/meshcat-python-mods",
    author="Robin Deits",
    author_email="mail@robindeits.com",
    license="MIT",
    packages=find_packages("src"),
    package_dir={"": "src"},
    test_suite="meshcatmods",
    entry_points={
        "console_scripts": [
            "meshcat-mods-server=meshcatmods.servers.zmqserver:main"
        ]
    },
    install_requires=[
      "ipython >= 5",
      "u-msgpack-python >= 2.4.1",
      "numpy >= 1.14.0",
      "tornado >= 4.0.0",
      "pyzmq >= 17.0.0",
      "pyngrok >= 4.1.6",
    ],
    zip_safe=False,
    include_package_data=True
)
