from setuptools import setup, find_packages

VERSION = '0.0.4'
DESCRIPTION = 'My very first Python package'
LONG_DESCRIPTION = 'My very first Python package with a slightly longer description'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="sample_testcoder",
    version=VERSION,
    author="Test Last",
    author_email="<testlast@email.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    python_requires='>=3',
    install_requires=["bpython", "numpy"],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)