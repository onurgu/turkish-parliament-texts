FROM python:3

WORKDIR /usr/src/app

COPY ./deployment/packagefiles/requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY ./   /usr/src/app/djangoproject/

RUN mkdir /usr/src/app/djangoproject/django_parliament/mappings &&\
    mkdir /usr/src/app/djangoproject/django_parliament/mappings/static


RUN mv /usr/src/app/djangoproject/resources/volumes/bower_components    /usr/src/app/djangoproject/django_parliament/mappings/static/ &&\
    mv /usr/src/app/djangoproject/resources/vendor                      /usr/src/app/djangoproject/django_parliament/mappings/static/

WORKDIR /usr/src/app/djangoproject/django_parliament

CMD python manage.py makemigrations &&\
    python manage.py migrate &&\

    python manage.py runserver 0.0.0.0:8000
