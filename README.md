# WeGroup Python Examination

Run the following commands in order to run the app with all the services

Note - If you are running the app localy, please change:

r = Redis(host='redis')
to r = Redis()

If not, please proceed with the following:

docker build -t "app" .
docker-compose up


If this is the 1st time, please set up the db:

docker exec -it exam_postgres_1 psql -U postgres
create database exam;
\connect exam
create table riskfactor(
zipcode integer primary key,
risk_factor varchar(1)
);
\q

You may need to restart the app by:

docker restart exam_app_1
