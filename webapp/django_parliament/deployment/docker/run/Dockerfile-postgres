FROM ubuntu:16.04

RUN apt-get -y update
RUN apt-get -y install postgresql=9.5+173ubuntu0.1 postgresql-contrib=9.5+173ubuntu0.1

USER postgres

RUN service postgresql start

RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.5/main/pg_hba.conf
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.5/main/postgresql.conf

CMD /usr/lib/postgresql/9.5/bin/postgres -D /var/lib/postgresql/9.5/main -c config_file=/etc/postgresql/9.5/main/postgresql.conf

