# Denial-of-Service simulator

Requirements:
* Python3
* Installation of `Flask` python library
* Installation of `Requests` python library

In a terminal (in an python environment of your preference: pyenv, pipenv, etc) run the following command:
```pip install Flask```
and:
```pip install requests```

## Client

To start the client you must supply the number of concurrent threads that will send requests to the server:
`python client.py 4` will start 4 concurrent threads, but you can specify any amount

For the client, the delay between each call for the same clientId was chosen to be between 0 and 1 second, you can change that value in line 29 of `client.py` file

## Server

Before starting the server, you will need to export the following environemnt variable: `FLASK_APP=server.py`
For example on Linux or MAC OSX terminal you can do it like this:
```
export FLASK_APP=server.py
```

And to start the server run:
```
flask run
```
