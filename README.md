# Introduction

A small repo (more of a gist) to help automate the process of :

- creating a package with a filter on a distance (dev) instance of AEM
- building the package
- download the package
  and then :
- uploading it onto you local instance of AEM
- install it

The code use only curls more or less.

# IMPORTANT

The code is really messy.
The dev instance server seems to have a timeout of 1 minute. So building a package should take less than that, otherwise, it failed

# Usage

Connect to your dev instance and find for the `login-token` cookie.
Rename the `.env.example` file to `.env` and replace the values with the correct ones.
Copy and paste it in a `.env` file in the root of the folder of this project.

The project use `poetry`, so run `poetry install` once and then run `poetry run python main.py` (or just `python main.py` if you already have activated the virtualenv).

Then you still need to clean all the created packages in dev by deleting them.
Also you can delete all .zip files downloaded in your local with `rm -rf *.zip`.
