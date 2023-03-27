# Elevator System 
An API based project created in django rest framework to manage an Elevator system


###  How to run it?

##### Installing requirements:
- Fork this project on your system
- Make sure you have Python installed, if not download from https://www.python.org/downloads/
- Download and install postgreSQL from https://www.postgresql.org/download/. Make sure to note your password and port.
- Download and install Postman from https://www.postman.com/downloads/
- 'cd' into the project directory and run command "pip install -r requirements.txt" to install all the python libraries being used in the project.

#### Setting up postgreSQL:
- After installing and setting up the pgadmin for Postgres, create a database in it by the name of 'elevatordb' 
insert image here
- Right Click on the PostgreSQL server, go to properties and under Connection tab you will see th e settings to connect to your database.
insert image here
- Go to settings.py file under the ElevatorSystemProject folder. In the below image a DATABASES setting is given. Add your password and port in that setting according to your password and port while setting up postgres
insert image here

#### Running the project:
- 'cd' into the project directory.
- On the terminal use command ```python manage.py makemigrations```
- Then use the command ```python manage.py migrate```
- Then to run the server use command ```python manage.py runserver```

