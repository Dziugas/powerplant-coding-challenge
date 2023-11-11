# Powerplant coding challenge

This api was build using Django Rest Framework. 

flake8 and black were applied for code style. 

No 3rd party library was used for calculations.

## Algorithm

The algorithm prioritizes power production with wind
(if there is any), as it has no cost and does not have minimum requirements for production.

If there is no wind, the other powerplants are sorted by calculated 
cost of producing 1MHw.

In case there is an over generation of power, then we adjust by 
looping through the selected for generation powerplants and reducing their production.

There is one test written, which takes into account the three payloads provided in the task description.

## Running the API

Build the container:

```docker build -t powerplants:latest .```

Run the container for development:

```docker run -p 8888:8888 -v .:/app powerplants```

Access the endpoint at:

```http://localhost:8888/api/productionplan/```