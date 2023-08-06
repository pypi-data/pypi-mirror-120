import setuptools
# from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup (
    name="infapy",                     # This is the name of the package
    version="1.0.5.5",                        # The initial release version
    author="Prashanth",                     # Full name of the author
    description="Automation Tool for informatica Cloud",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    #packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.7',                # Minimum version requirement of the package
    package_dir = {
            'infapy': 'infapy',
            'infapy.v2': 'infapy/v2',
            'infapy.v3': 'infapy/v3',
            'infapy.cdi': 'infapy/cdi'},
    packages =["infapy","infapy.v2","infapy.v3","infapy.cdi"],             # Name of the python package
    # clspackage_dir={'infapy':''},     # Directory of the source code of the package
    install_requires=["requests","cryptography"]                     # Install other dependencies if any
)