# MEHRA INTERVIEW

a task to create a CRUD application for product managing 

## Features 
1. implementing jwt authentication using simple-jwt library
2. only product owners can manipulate their products 
3. CRUD implementation for product entity using APIView abstract class

## Requirements 
+ python >= 3.11
## Run
1. install required packages using pip
``` 
python -m pip install -r requirements.txt
```
2. apply the migrations 
```
python manage.py migrate
```
3. run the application using python
```
python manage.py runserver
```

## Test 

+ authentication tests file : my_auth/tests.py 
+ product tests file : product/tests.py

1. run the authentication tests using python
```
python manage.py test my_auth
```

2. run the products tests
```
python manage.py test product
```
**there will be no error with the tests** 


## swagger 
for accessing swagger api documentation run the project and then visit the url below: 
```
http://localhost:8000/swagger/
```

## redoc 
for accessing redoc api documentation run the project and then visit the url below : 
```
http://localhost:8000/redoc/
```

