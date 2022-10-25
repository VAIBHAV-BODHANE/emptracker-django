# emptracker-django

* Python (3.6, 3.7, 3.8, 3.9)
* Django (2.2, 3.0, 3.1)

We **highly recommend** and only officially support the latest patch release of
each Python and Django series.


## Installation
The first thing to do is to clone the repository:

```sh
$ https://github.com/VAIBHAV-BODHANE/emptracker-django.git
$ cd emptracker-django
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv -p python3 venv
$ source env/bin/activate
```
Then install the dependencies:

```sh
(venv)$ pip install -r requirements.txt
```
Note the `(venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv`.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ python manage.py migrate
(env)$ python manage.py runserver
```

## For signup and login in the web application there is a pattern which we should maintain like xyz@ourorg.in (@ourorg.in) and for admin registration pattern should be xyzadmin@ourorg.in and most important admin registration only can happen through terminal with command below
```sh
$ python manage.py createsuperuser
