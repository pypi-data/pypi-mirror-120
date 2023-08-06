from setuptools import setup, find_packages

setup(
    name="hisock",
    version="0.0.1.post2",
    description="A higher-level extension of the socket module, with simpler and more efficient usages",
    url="https://github.com/SSS-Says-Snek/hisock",
    author="SSS-Says-Snek",
    author_email="bmcomi2018@gmail.com",
    license="MIT",
    install_requires=[
        "pytest>=6.2.5",
        "cryptography>=3.4.8"
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src")
)
