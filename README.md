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

## API Endpoints and Playing around with the project
Follow the below steps in the presented order

#### Admin User
- For the first step, you will need to create an admin user. For that send a post request to the end point ```http://127.0.0.1:8000/admin-user/create``` using Postman. You will need a response body which looks like {"email":"yourEmail@email.com", "password":"Your password"}.
- When that user is created, you will be able to use that user credentials to create elevators and register a number of floors for the building

#### Register Floors
- To register a number of floors for the building you will need to send a post request to the end point ```http://127.0.0.1:8000/floor/create``` using Postman. You will need Basic Auth Headers in Postman which will contain the details of your admin user as username and password. You will also need a response body which will contain the number of floors you wish to register which will look like {"NumberOfFloors":number}.

#### Creating Elevators
- To create elevators for the building you will need to send a post request to the end point ```http://127.0.0.1:8000/elevator/create``` using Postman. You will need Basic Auth Headers in Postman which will contain the details of your admin user as username and password. You will also need a response body which will contain the number of elevator you wish to create which will look like {"n":number}.

#### Rest of the endpoints
Rest of the endpoints can be triggered in any order. They are mentioned below:

###### To request an elevator on a floor
- You will need to send a get request on the endpoint ```http://127.0.0.1:8000/floor/<floorNumber>/request-elevator?destination=<destinationFloorNumber>``` using Postman, where the 'floorNumber' will be replaced by the floor you need to request the elevator from, and the 'destinationFloorNumber' to be replaced by the floor number where you want the elevator to go.
- This will return an elevator assigned optimally for the requested floor

###### To get the request list of an elevator
- You will need to send a get request on the endpoint ```http://127.0.0.1:8000/elevator/<label>/request-list``` using Postman, where the 'label' will be replaced by the elevator label of which you want the request list.
- You will need Basic Auth Headers in Postman which will contain the details of your admin user as username and password.
- This will return a list of floors assigned to the mentioned elevator.