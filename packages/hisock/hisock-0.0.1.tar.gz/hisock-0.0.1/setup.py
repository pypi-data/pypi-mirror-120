from setuptools import setup

import constants

with open("requirements.txt") as read_req:
    required_packages = read_req.readlines()

setup(
    name="hisock",
    version=constants.__version__,
    description="A higher-level extension of the socket module, with simpler and more efficient usages",
    url="https://github.com/SSS-Says-Snek/hisock",
    author="SSS-Says-Snek",
    author_email="bmcomi2018@gmail.com",
    license="MIT",
    install_requires=required_packages
)
