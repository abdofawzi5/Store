# Stocky
![alt text](https://preview.ibb.co/eaaXOe/Screenshot_from_2018_09_30_02_34_28.png "Dashboard")

Stocky is Stock Management System, Built using [Django framework](https://www.djangoproject.com/)

## Why Stocky

You can use this project to Add, edit and manage all these models
1. Company information.
2. Branches.
3. Branches managers and their permissions.
4. Products.
5. Product quantities
6. Imports.
7. Sales.
8. Invoices.

The project contains a dashboard to 
1. Review all remaining quantities.
2. Charts to show progress.
3. Filter using a date to review how was your progress on this date. 

## Technologies 
To build this project we used several technologies
1. [Django framework](https://www.djangoproject.com/)
2. [MySQL](https://www.mysql.com/)
3. [Docker](https://www.docker.com/)
4. Wkhtmltopdf package

### Installation
#### Add envirnoment vriables
copy `.env.example` to `.env` and fill the values of the variables, Example
```bash
# MySQL Env. variables
MYSQL_ROOT_PASSWORD=root
MYSQL_DATABASE=django-dbname
MYSQL_USERNAME=root
MYSQL_PASSWORD=root

# Database host
DB_HOST=db
DB_PORT=3306
```

#### Install and run docker
The benefit to having docker in your project is you don't need to worry about dependencies, just install [docker](https://docs.docker.com/install/), [docker-compose](https://docs.docker.com/compose/install/) and [docker-machine](https://docs.docker.com/machine/install-machine/) then run
```console
$ docker-compose build
$ docker-compose up
```

#### Run
1. Create superuser for login
```console
$ docker-compose exec web python manage.py createsuperuser
```
2. to generate random data for testing

```console
$ docker-compose exec web python generateData.py
```






