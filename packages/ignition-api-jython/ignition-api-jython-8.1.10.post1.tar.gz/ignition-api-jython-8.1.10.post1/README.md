# Ignition

<!--- Badges --->
![GitHub last commit (jython)](https://img.shields.io/github/last-commit/thecesrom/Ignition/jython)
[![GitHub contributors](https://img.shields.io/github/contributors/thecesrom/Ignition)](https://github.com/thecesrom/Ignition/graphs/contributors)
[![GitHub license](https://img.shields.io/github/license/thecesrom/Ignition)](https://github.com/thecesrom/Ignition/blob/jython/LICENSE)
[![GitHub downloads](https://img.shields.io/github/downloads/thecesrom/Ignition/total)](https://github.com/thecesrom/Ignition/releases)
[![time tracker](https://wakatime.com/badge/github/thecesrom/Ignition.svg)](https://wakatime.com/badge/github/thecesrom/Ignition)
[![Sourcery](https://img.shields.io/badge/Sourcery-enabled-brightgreen)](https://sourcery.ai)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Imports: flake8](https://img.shields.io/badge/%20imports-flake8-%231674b1?style=flat&labelColor=ef8336)](https://flake8.pycqa.org/en/latest/)
[![Join us on GitHub discussions](https://img.shields.io/badge/github-discussions-informational)](https://github.com/thecesrom/Ignition/discussions)

Ignition is a set of packages and modules that allows developers to get code completion for Ignition Scripting API scripting functions in their IDE of choice.

# Releases

Check the [releases page](https://github.com/thecesrom/Ignition/releases) and download the one for your current version.

If you can't find it, feel free to submit your request on our [Discussions](https://github.com/thecesrom/Ignition/discussions).

## Prerequisites

Before you begin, ensure you have met the following requirements:

* Java 11
  * From [Azul](https://www.azul.com/downloads/?version=java-11-lts&package=jdk)
  * Or with Homebrew on macOS
    ```bash
    $ brew install --cask zulu11
    ```
* Jython
  * 2.7.1 for Ignition 8.0 through 8.1.7
    * Download [here](https://search.maven.org/remotecontent?filepath=org/python/jython-installer/2.7.1/jython-installer-2.7.1.jar)
    * Or via Homebrew
      ```bash
      $ brew install coatl-dev/coatl-dev/jython@2.7.1
      ```
  * 2.7.2 for [Ignition 8.1.8 onwards](https://docs.inductiveautomation.com/display/DOC81/New+in+this+Version#NewinthisVersion-Newin8.1.8)
    * Download [here](https://search.maven.org/remotecontent?filepath=org/python/jython-installer/2.7.1/jython-installer-2.7.2.jar)
    * Or via Homebrew
      ```bash
      $ brew install coatl-dev/coatl-dev/jython@2.7.2
      ```
* You are familiar with [Ignition 8.1 System Functions](https://docs.inductiveautomation.com/display/DOC81/System+Functions)

## Packages

Ignition consists of the following packages:

* com
* system

### com

These are libraries for some of Inductive Automation's Java packages and functions that are imported in `system` packages.

### system

Is a package that includes all Ignition Scripting Functions.

## Installation and usage

The preferred method is to install it by running `pip` by running `jython -m pip install` like this:

```bash
$ jython -m pip install https://github.com/thecesrom/Ignition/archive/refs/tags/v8.1.10-jython.post1.zip
```

This will install it as package to your Jython installation, which will allow you to call Ignition Scripting functions from Jython's REPL.

```bash
$ jython
Jython 2.7.2 (v2.7.2:925a3cc3b49d, Mar 21 2020, 10:03:58)
[OpenJDK 64-Bit Server VM (Azul Systems, Inc.)] on java11.0.12
Type "help", "copyright", "credits" or "license" for more information.
>>> from __future__ import print_function
>>> import system.util
>>> print(system.util.__doc__)
Utility Functions.

The following functions give you access to view various Gateway and
Client data, as well as interact with other various systems.


>>> system.util.beep()
>>> quit()
```

And to uninstall:

```bash
$ jython -m pip uninstall ignition-api-jython
```

### Downloading from releases

You may also download the code targeted to your desired version from the [releases page](https://github.com/thecesrom/Ignition/releases) and add it as a dependency to your scripting project.

## Contributing to Ignition

To contribute to Ignition, follow these steps:

1. Fork this repository
2. Create a local copy on your machine
3. Create a branch
4. Make your changes and commit them
5. Push to the original branch
6. Create the pull request

Alternatively see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## Contributors

Thanks to everyone who has contributed to this project.

Up-to-date list of contributors can be found [here](https://github.com/thecesrom/Ignition/graphs/contributors).

## License

See the [LICENSE](https://github.com/thecesrom/Ignition/blob/HEAD/LICENSE).

## Code of conduct

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
