DIR=$PWD/`dirname $0`

docker volume create --name django_parliament_postgresql-volume
docker volume create --name django_parliament_migrations-volume


docker build -f $DIR/init/Dockerfile-init-postgres -t django_parliament_init_postgres_i $DIR/../../../django_parliament
docker build -f $DIR/init/Dockerfile-init-django -t django_parliament_init_django_i $DIR/../../../django_parliament


docker-compose -f $DIR/init/docker-compose-init-postgres.yml up -d
echo "Wait for 20s"
sleep 20s
docker-compose -f $DIR/init/docker-compose-init-django.yml up -d
echo "Wait for 40s"
sleep 40s


docker rm -f django_parliament_django_c
docker rm -f django_parliament_postgres_c


docker network rm init_default


rm -rf $DIR/../../resources/volumes/migrations
cp -r /var/lib/docker/volumes/django_parliament_migrations-volume/_data $DIR/../../resources/volumes/migrations
docker volume rm -f django_parliament_migrations-volume

rm -rf $DIR/../../resources/volumes/postgres_main
mv /var/lib/docker/volumes/django_parliament_postgresql-volume/_data $DIR/../../resources/volumes/postgres_main
docker volume rm -f django_parliament_postgresql-volume