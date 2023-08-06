
import setuptools
from distutils.core import setup

with open('README.md', 'r') as f:
    long_description = f.read()

pkg_info = {}
with open('src/ota/_version.py', 'r') as f:
    exec(f.read(), pkg_info)

setup(
    name="pycom-ota-client",
    version=pkg_info['__version__'],
    description="Pycom OTA firmware client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="snebot",
    author_email="snebot@bitgrup.com",
    url="https://github.com/snebot-bg/pycom-ota-client",
    keywords=[],
    classifiers=[],
    package_dir={ "": "src" },
    packages=setuptools.find_packages(where="src"),
    install_requires=['bg-urequests']
)
