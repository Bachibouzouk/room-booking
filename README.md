# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* Summary of set up

Setup a virtualenv with python 3 (I used python3.4).

On windows (10 at least), installing virtualenv

```
#!python
c:\python34\python -m pip install virtualenv
```
Creating a virtualenv
```
#!python
c:\python34\python -m virtualenv <virtual_env_dir>
```
using the virtualenv
```
#!python
<virtual_env_dir>\Scripts\activate.bat
```

On linux
Creating a virtualenv
```
#!python
virtualenv --python=python3.4 .virtualenv/"my custom name"
```
using the virtualenv
```
#!python
source .virtualenv/"my custom name"/bin/activate
```

* Configuration
* Dependencies

Go into the repo and pip install django and numpy

* Database configuration
run 
```
#!python

python manage.py migrate
```

* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact