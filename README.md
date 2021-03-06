################
Airport Distance
################

airport_distance is a python shell program that will read in the distances between a list of airports, and then calculate the shortest path between the two airports which have been entered.

###Usage
To call with the default airport list, simply run the program. You will be prompted to put in the source and destination airport in a single prompt. The program expects that the input is entered in the format "DEP -- ARR", where DEP is the three letter code for the destination airport, and ARR is the three letter code for the arrival airport.

To use a seperate list of airports, you can pass in the path to the file as the first parameter to the script, e.g.

_____
./airport_distance /home/diarmaid/boxever/Airports.csv
_____

The airport file is expected to have at least three columns, with the departure airport column labelled "Dep", the arrival airport column labelled "Arr", and the time taken to fly between the airports labelled "Time".   

The default seperator that is used is ";". This can be changed by passing it in as the second command line argument, e.g.

____
./airport_distance.py /home/diarmaid/boxever/Airports.csv ","
___

###Requirements
Python3 is required to run the script.   On most linux distributions, this is already provided. On Windows, you have to download and install it first.

In order to run the script, the pandas library and the networkx library need to be installed. To install, run
___
pip3 install networkx pandas
___
Alternatively, install the dependencies for both the script and the testing by running
___
python3 -m pip install -r requirements.txt
___

###TESTS
To run the tests, the mock library is also required. Install it using
___
pip3 install mock
___

To run the tests, run
___
python3 test_airport_distance.py
___

###Errors
When the airports are not in the graph, or there is no shortest path found, this will return "No path found".

###Reflections
This uses networkx to define the graph and run the graph operations.   Networkx is slow - one to two orders of magnitude slower than equivilent C++ libraries (e.g. SNAP). If you are calculating the distance between a large number of airports, it could be worthwhile to reimplement this in a faster library - snap has Python support, or there are many different alternatives out there.  For small airport lists (~ few thousands) this should will not matter much.

This currently uses Dijiska algorthm (as implemented by NetworkX) to calculate the shortest path.   This is of the order of N squared, where N is the number of nodes in the graph (the number of airports).   For large numbers of airports with sparse flights between them, a different algorthm could be better - e.g. the order of (E + N), where N is the number of nodes and E is the number of edges. 

