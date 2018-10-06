DIR=$PWD/`dirname $0`

docker build -f $DIR/run/Dockerfile-django -t django_parliament_django_i $DIR/../../../django_parliament

docker-compose -f $DIR/run/docker-compose-run-django.yml up -d
