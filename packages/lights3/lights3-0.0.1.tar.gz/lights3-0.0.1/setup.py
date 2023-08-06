try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import re

version = re.search(
    '^__version__\s*=\s*"(.*)"', open("lights3/lights3.py").read(), re.M
).group(1)

with open("README.md", "rb") as f:
    description = f.read().decode("utf-8")

setup(
    name="lights3",
    packages=["lights3"],
    python_requires=">=3",
    entry_points={"console_scripts": ["lights3 = lights3.lights3:main"]},
    version=version,
    description="Lightweight S3 toolkit",
    long_description=description,
    long_description_content_type="text/markdown",
    author="Khalil Muhammad",
    author_email="micaleel@gmail.com",
    url="https://github.com/micaleel/lights3",
    license="MIT",
    keywords=[
        "AWS",
        "S3",
    ],
    install_requires=["boto3",],
)