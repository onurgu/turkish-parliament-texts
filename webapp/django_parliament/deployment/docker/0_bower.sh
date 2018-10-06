DIR=$PWD/`dirname $0`


docker volume create --name django_parliament_bower-volume


docker build -f $DIR/init/Dockerfile-init-bower -t django_parliament_init_bower_i $DIR/../../../django_parliament
docker-compose -f $DIR/init/docker-compose-init-bower.yml up -d


docker rm -f django_parliament_bower_c
docker network rm init_default


rm -rf $DIR/../../resources/volumes/bower_components
cp -r /var/lib/docker/volumes/django_parliament_bower-volume/_data $DIR/../../resources/volumes/bower_components
docker volume rm -f django_parliament_bower-volume