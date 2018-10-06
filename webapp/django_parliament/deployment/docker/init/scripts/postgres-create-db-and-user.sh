psql --command "CREATE DATABASE psqldb" &&\
psql --command "CREATE USER psqluser WITH PASSWORD 'psql1234';" &&\
psql --command "ALTER ROLE psqluser SET client_encoding TO 'utf8';" &&\
psql --command "ALTER ROLE psqluser SET default_transaction_isolation TO 'read committed';" &&\
psql --command "ALTER ROLE psqluser SET timezone TO 'UTC';" &&\
psql --command "GRANT ALL PRIVILEGES ON DATABASE psqldb TO psqluser;"