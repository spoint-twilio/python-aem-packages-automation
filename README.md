# AEM Package Automation

## Introduction

A small repo (more of a gist) to help automate the process of :

- creating a package with a filter on a distant (dev) instance of AEM.
- building the package.
- download the package.
  and then :
- uploading it onto you local instance of AEM.
- install it.

More or less, the script is only a sequence of "curl" commands.

## IMPORTANT

The code is really messy.
The dev instance server seems to have a timeout of 1 minute.
So building a package should take less than that, otherwise, it failed.

## Usage

1. Copy/Paste the `.env.example` into a `.env` file.
2. Connect to your dev instance and look for the `login-token` cookie. Copy the value.
3. Replace all the values of the `.env` file with the correct ones.
4. If not already installed, install `poetry`.
   Then you can install deps with `poetry install`.
5. Edit the `helpers/package_names_and_filters.py` file to match the packages you want to create/process.
   Please remember that due to the 1minute timeout, the package should be quick to build.
   Follow the tuple format `("package-name", "filter-path")`.
6. Run the script with `poetry run python main.py`.
