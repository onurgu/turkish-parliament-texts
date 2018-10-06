docker rm -f $(docker ps -aq)
docker network prune -f
docker volume prune -f

DIR=$PWD/`dirname $0`
rm -rf $DIR/../../resources/volumes/migrations
rm -rf $DIR/../../resources/volumes/bower_components
rm -rf $DIR/../../resources/volumes/postgres_main