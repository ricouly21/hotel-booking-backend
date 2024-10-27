## 1. Create shared network
First, create the shared network `app_network` on Docker.
```
docker network create app_network
```

## 2. Run the Provider service
Go to the `provider` directory and run the docker compose file.
```
cd provider/
docker compose up --build -d
```

This will both initialize the **PostgreSQL** database and the **Provider** service.
If you want to verify that the database has been properly initialized, you can run this command.
```
docker exec -it postgres psql -U app_user app_db -c "select * from provider_event;"
# Press 'd' to scroll down through the database table.
# Hit 'q' to exit the console
```

### Testing
You can run the unit tests of the service by running this command:
```
docker exec -it provider python manage.py test
```
You can also test the API service using the Swagger documentation.
> Link to Swagger doc: http://0.0.0.0:8000/swagger/

## 3. Run the Dashboard service
Go to the `dashboard` directory and run the docker compose file.
```
cd dashboard/
# or cd ../dashboard if you're currently in the provider directory

# Then run the docker compose file.
docker compose up --build -d
```

This will initialize the **Dashboard** service.

### Testing
You can run the unit tests of the service by running this command:
```
docker exec -it dashboard python manage.py test
```
You can also test the API service using the Swagger documentation.
> Link to Swagger doc: http://0.0.0.0:8080/swagger/