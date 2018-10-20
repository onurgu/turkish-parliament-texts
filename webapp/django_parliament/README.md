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

#### Explanation

0_bower.sh : Bu bir container yaratip bower ile js library'lerini indirip, resources/volumes/bower_components'in icine docker volume ile map ediyor.

1_volume.sh : Bu bir postgres user'i yaratiyor django baglanabilsin diye. Django icin gerekli database tablolarini yaratip migration'lari yaratiyor ve postgres'e ekliyor. Django'da admin:admin diye bir superuser olusturuyor. Ve bu postgres datasi volume'unu resources/volumes/postgres_main dizinine, django migrationlarini da resources/volumes/migrations dizinine map ediyor.

2_postgres.sh : resources/volumes/postgres_main dizini ile docker volume baglantisi olusturup, postgres'i ayaga kaldiriyor. volume mapping'den dolayi postgres user ve django tablolari hazir zaten.

3_django.sh : Bu da javascript dosyalarini django'nun anlayacagi bir dizine tasiyor.
migrationlar icin bir docker volume baglantisi olusturuyor; bu sayede daha sonra bunlari ve postgres docker volume'unu baska bir bilgisayara aktarip ayni kurulum yapilabilir.
django kodlari ile docker volume baglantisi olusturuyor. bu sayede container'da degil de bilgisayardaki kodu mesela pycharm ile editleyip kaydedince, docker'in icindeki kod da guncellenmis oluyor kendiliginden, tekrar build etmeden.
ve en nihayetinde django'yu 8000 portunda, ayaga kaldiriyor.



yeni bir bower paket'i eklemek icin, deployment/packagefiles/bower.txt'ye paketi yazmak, 0_bower.sh ve sonra 3_django.sh'i calistirmak gerekiyor.

yeni bir python paket'i eklemek icin, deployment/packagefiles/requirements.txt'ye paketi yazmak, ve 3_django.sh'i calistirmak gerekiyor.

resources/volumes dosyasi gitignore'a ekli. bir makinedeki database'i tasimak icin, resources/volumes'u kopyalayip 2.sh ve 3.sh scriptlerini calistirmak yeterli olmali.

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
