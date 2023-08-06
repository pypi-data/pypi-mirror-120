# ndn4sid

A first implementation of ndn4sid.



## Installation

Run the following command to install:

```
pip install ndn4sid
```

## Usage
The source folder contains a directory with examples.


## Testing
In order to run the tests, install the package with the [dev] option.
This is done via the command
```
pip install "nd4sid[dev]"
```
To test the current version of the code on your machine, you can run
```
pytest
```
To do a full test of the code use ```tox```
```
tox
```

## Steps to update the code 
Update the manifest file to include all files in de final project 
```
check-manifest --update
```
Compile the latest version of the code
```
python setup.py bdist_wheel sdist
```
Upload the code to Pypi, make sure to update the build number. 
```
twine upload --skip-existing dist/*
```
