FROM python:3

WORKDIR /usr/src/app

COPY ./deployment/packagefiles/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./   ./djangoproject/

RUN mkdir ./djangoproject/django_parliament/mappings &&\
    mkdir ./djangoproject/django_parliament/mappings/migrations &&\
    touch ./djangoproject/django_parliament/mappings/migrations/__init__.py

WORKDIR /usr/src/app/djangoproject/django_parliament

CMD python manage.py migrate &&\

    python manage.py shell < ../deployment/docker/init/scripts/django-create-admin.py &&\

    python manage.py runserver