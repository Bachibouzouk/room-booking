### What is this repository for? ###

* This repository is a proposal for a room-booking app, allowing users to consult availability and reserve rooms. It was created for showcase to McGill administrators.
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

* How to write commands to test your code
Go into the folder "room_booking/room_display/management/commands/"
Then create a ".py" file in which you run some code (like create an object and call its methods). You can execute that by typing :
```
#!python

python manage.py your_code_file_name_without_extension
```

* Deployment instructions

### Contribution guidelines ###

* Writing tests

write tests in the room_booking/room_display/test.py file, to run them type 
```
#!python

python manage.py test room_display 
```

* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin : pfduc@physics.mcgill.ca
* Other community or team contact
