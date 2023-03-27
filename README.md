# Elevator System 
An API based project created in django rest framework to manage an Elevator system

### Video Demo Link
https://drive.google.com/file/d/1kRkCvwuj4s1dxPfQijmlcM2-ArBapOaO/view?usp=sharing

###  How to run it?

##### Installing requirements:
- Fork this project on your system
- Make sure you have Python installed, if not download from https://www.python.org/downloads/
- Download and install postgreSQL from https://www.postgresql.org/download/. Make sure to note your password and port.
- Download and install Postman from https://www.postman.com/downloads/
- 'cd' into the project directory and run command "pip install -r requirements.txt" to install all the python libraries being used in the project.

#### Setting up postgreSQL:
- After installing and setting up the pgadmin for Postgres, create a database in it by the name of 'elevatordb' 

![Postgres create db](https://user-images.githubusercontent.com/51481039/227950091-f1850819-9bfd-4877-9123-cb32732bf4e6.PNG)

- Right Click on the PostgreSQL server, go to properties and under Connection tab you will see th e settings to connect to your database.

![postgres connection properties](https://user-images.githubusercontent.com/51481039/227950162-d678f3ce-3521-4e48-9626-eec78224cc0e.PNG)

- Go to settings.py file under the ElevatorSystemProject folder. In the below image a DATABASES setting is given. Add your password and port in that setting according to your password and port while setting up postgres

![django settings](https://user-images.githubusercontent.com/51481039/227950209-45c10729-fc30-4f0f-b270-e02fdde3c4e4.PNG)

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

###### To mark the elevator as active/under maintenance
- You will need to send a post request on the endpoint ```http://127.0.0.1:8000/elevator/<label>/set-status``` using Postman, where the 'label' will be replaced by the elevator label of which you want to change the status.
- You will need Basic Auth Headers in Postman which will contain the details of your admin user as username and password.
- You will also need a response body which will contain the status for the elevator which will look like {"status":true/false}.true for active, false for under maintenance

#### To make the elevator go up and down
- You will need to send a post request on the endpoint ```http://127.0.0.1:8000/elevator/<label>/up``` using Postman, where the 'label' will be replaced by the elevator label which you want to go up.
- To make the elevator fo down, You will need to send a post request on the endpoint ```http://127.0.0.1:8000/elevator/<label>/down``` using Postman, where the 'label' will be replaced by the elevator label which you want to go down.

#### To start/stop the elevator
- You will need to send a post request on the endpoint ```http://127.0.0.1:8000/elevator/<label>/change-moving``` using Postman, where the 'label' will be replaced by the elevator label which you want to start/stop.
- If the elevator passed was already in motion, it will stop. If the elevator was already stopped it will start.

#### To open/close the elevator doors
- You will need to send a post request on the endpoint ```http://127.0.0.1:8000/elevator/<label>/open-door``` using Postman, where the 'label' will be replaced by the elevator label of which you want to open the doors.
- To make the elevator fo down, You will need to send a post request on the endpoint ```http://127.0.0.1:8000/elevator/<label>/close-door``` using Postman, where the 'label' will be replaced by the elevator label of which you want to open the doors.

#### To get an elevator's current floor
- You will need to send a get request on the endpoint ```http://127.0.0.1:8000/elevator/<label>/current-floor``` using Postman, where the 'label' will be replaced by the elevator label of which you want to get the current floor.

#### To get an elevator's next destination floor
- You will need to send a get request on the endpoint ```http://127.0.0.1:8000/elevator/<label>/next-destination``` using Postman, where the 'label' will be replaced by the elevator label of which you want to get the next destination floor.

#### To see if an elevator is going up or down
- You will need to send a get request on the endpoint ```http://127.0.0.1:8000/elevator/<label>/movement``` using Postman, where the 'label' will be replaced by the elevator label of which you want to see if it is going up or down.

## Model Structure
In this project, we are using 3 tables, 1 for admin users, 1 for floors and 1 for elevators

- ADMIN USERS : email, username(same as email), password
- FLOOR : floorNumber(unique for every floor, e.g. 1,2)
- ELEVATOR : label(unique for every elevator), status(to mark an elevator as active/under maintenance), currentFloor, moving(to see if an elevator is stopped or not), requestList(Many to Many List to see how many floors are assigned to an elevator)
