DIR=$PWD/`dirname $0`

docker build -f $DIR/run/Dockerfile-postgres -t django_parliament_postgres_i $DIR/../../../django_parliament

docker-compose -f $DIR/run/docker-compose-run-postgres.yml up -d

sleep 15s