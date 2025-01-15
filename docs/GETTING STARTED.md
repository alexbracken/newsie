# Getting Started
These instructions are primarily for those using MacOS. I'm on Sequoia (15.2), and these instructions are based on that system.

# Prerequisities
- Python 3.14
- [Poetry](https://python-poetry.org/docs/) (dependency management)

## Download script
### Method 1: Using git
If you already have git installed, clone the repository into a folder on your machine.

```sh
git clone https://github.com/alexbracken/newsie.git
```
The ``clone`` command will create a new directory in the location of the terminal, so you may need to use the ``cd`` command to 
### Method 2: Using Github website
Download the latest release from the [releases page](https://github.com/alexbracken/newsie/releases) of the repository, and unzip at the location.

## Install dependencies with Poetry

This package requires the following Python modules be installed. This project uses [Poetry](https://python-poetry.org/docs/), a dependency management tool.
1. Install Poetry using the installation script.
    ```sh
    curl -sSL https://install.python-poetry.org | python3 -
    ```
2. Test Poetry installation
    ```sh
    poetry --version
    ```
3. Install dependencies
    ```sh
    poetry install
    ```
### Alternate method (not recommended)
You can install the following packages individually using:
```sh
pip install [package name]
```
  - python-facebook-api
  - feedparser
  - requests
  - python-dotenv
  
The disadvantage of this method is you lose the ability to isolate the program from your global installation, which may have different requirements that conflict with this package.

## Script Setup

