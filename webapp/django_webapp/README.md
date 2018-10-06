# django_parliament

## 1. Introduction

The project is designed based on the Django framework. Postgresql and Docker are used in the project.

<br/>

Django can be a very useful framework. 
- Django simplifies database operations. 
  - Required lines of codes to manage database are very few.
  - Data read and write operations are done with one line of code.
  - Table structures are implemented in "models.py".  
- Django simplifies url management.
- For UI implementation, Django has a template language.

<br/>

However, to prepare the system for the first time, there are lots of things to do.
- Prepare python virtual environment and manage requirements
- Configure settings.py
  - allauth django application for login system
  - database settings; database engine, database name, user name, user password, host, port
  - static files folder path
- Configure urls.py; admin urls, application urls, login urls
- Download javascript libraries
- Implement index page; html file, url mapping, view url directing

<br/>

In this template project, mentioned first time steps are handled and overhead part of the Django framework is skipped.

Django configurations are prepared, including database settings and Javascript libraries are downloaded with bower.

In addition to that, to run and deploy the project, Docker is used. Django and Postgres dockerfiles are implemented.
- Python packages are installed within the docker image.
- Volumes are created for database, django migrations and javascript libraries.
- With database volume, database can be backed up and deployed to another machine easily.
- Project deployment is automatized.

## 2. Prerequisites
- Docker

## 3. Preprocessing

- Set project and application name
```bash
python ./setup/rename/renameProjectAndApplication.py project_name application_name
```

## 4. Installation

```bash
bash ./setup/docker/0_bower.sh
bash ./setup/docker/1_volume.sh
bash ./setup/docker/2_postgres.sh
bash ./setup/docker/3_django.sh
```

## 5. Guidelines

#### Implementation

When there is a change in code, ./setup/docker/**3_django.sh** script must be run.

#### Python Libraries

Python libraries are managed with ./resources/requirements.txt file.

When a library is added or removed in requirements.txt file, ./setup/docker/**3_django.sh** script must be run.

#### Javascript Libraries

Javascript libraries are managed with ./resources/bower.txt file. 
Valid entry formats are "lib_name" and "lib_name#version". 

When a library is added or removed in bower.txt file, ./setup/docker/**0_bower.sh** script must be run. 
With this, docker volume for bower will be updated.

Bower volume is mapped to ./main_app/static/bower_components/ directory. Installed libraries reside in the folder. In html files, library source paths are written as "/static/bower_components/lib_path/lib.js".

#### Database Export and Import

Database export is easy with docker volumes. Docker volumes path in Linux is /var/lib/docker/volumes.

Database data path is /var/lib/docker/volumes/django_parliament_postgresql-volume. Just copy and save the directory.

<br/>

Database import is also easy. Copy saved directory to /var/lib/docker/volumes/django_parliament_postgresql-volume.

And then run ./setup/docker/**2_postgres.sh** script. 
