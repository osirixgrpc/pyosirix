---
pyOsirix
---

[![image](https://img.shields.io/badge/pypi-v0.1.6-green)](https://pypi.org/project/pyosirix/)

[comment]: <> ([![image]&#40;https://img.shields.io/travis/timothy22000/pyosirix.svg&#41;]&#40;https://app.travis-ci.com/github/timothy22000/pyosirix&#41;)

[comment]: <> ([![Updates]&#40;https://pyup.io/repos/github/osirixgrpc/pyosirix/python-3-shield.svg&#41;]&#40;https://pyup.io/account/repos/github/osirixgrpc/pyosirix/&#41;)
[![Updates](https://pyup.io/repos/github/timothy22000/test_cookiecutter/python-3-shield.svg)](https://pyup.io/account/repos/github/timothy22000/test_cookiecutter/) 


**Table of contents**

* [PyOsirix and gRPC](#pyosirix)
* [Installation](#installation)
* [Development](#development)
* [Bug/Feature Request](#feature-request)
* [To-do](#todo)
* [Credits](#credits) 


## PyOsirix and gRPC
This provides a Pythonic interface that uses the osirixgRPC plugin to interact with OsiriX and Horos, to provide access to functionality through the gRPC protocol.  This will supercede the previous implementation of pyOsiriX as it will be general, and easy to maintain.

-   Free software: BSD license
-   Documentation:
    <https://osirixgrpc.github.io/>

## Installation

**Requirements**

* Python 3+ (https://www.python.org/)
* Horos/Osirix (https://horosproject.org/)

**Instructions**

Using pip:
```
pip install pyosirix
```

Using it from github for development purposes:
```bash

git clone git@github.com:osirixgrpc/pyosirix.git
cd pyosirix
pip install -r requirements.txt
# Create your own scripts with main function to test the functionality, note that you need to start an OsirixService first and have Horos/Osirix open.
# See unit tests for examples

```
## Features

-   TODO

## Development
Want to contribute? Great! We always welcome contributions from interested developers.

To fix a bug or enhance an existing module, follow these steps:

- Fork the repo
- Create a new branch (`git checkout -b improve-feature`)
- Make the appropriate changes in the files
- Add changes to reflect the changes made
- Commit your changes (`git commit -am 'Improve feature'`)
- Push to the branch (`git push origin improve-feature`)
- Create a Pull Request

## Bug / Feature Request

If you find a bug (the website couldn't handle the query and / or gave undesired results), kindly open an issue [here](https://github.com/osirixgrpc/pyosirix/issues) by including your search query and the expected result.

If you'd like to request a new function, feel free to do so by opening an issue [here](https://github.com/osirixgrpc/pyosirix/issues/new). Please include sample queries and their corresponding results.

## To-do
- Placeholder

## Credits

* Timothy Sum Hon Mun <timothy22000@gmail.com/ timothy.sumhonmun@icr.ac.uk>
* Matthew Blackledge <mattyblackledge@gmail.com/ matthew.blackledge@icr.ac.uk>
