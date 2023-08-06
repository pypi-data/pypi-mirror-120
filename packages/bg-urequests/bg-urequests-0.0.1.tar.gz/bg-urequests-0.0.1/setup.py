
import setuptools
from distutils.core import setup

with open('README.md', 'r') as f:
    long_description = f.read()

pkg_info = {}
with open('src/urequests/_version.py', 'r') as f:
    exec(f.read(), pkg_info)

setup(
    name="bg-urequests",
    version=pkg_info['__version__'],
    description="Basic MicroPython HTTP request library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="snebot",
    author_email="snebot@bitgrup.com",
    url="https://github.com/snebot-bg/urequests",
    keywords=[],
    classifiers=[],
    package_dir={ "": "src" },
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6"
)
