#!/usr/bin/env python3
import pandas as pd
import networkx as nx
from typing import Tuple, Union, List
import sys

def read_in_graph(path: str, seperator: str= ";") -> nx.DiGraph:
    """Read in the file stored in path and return the associated graph

    The file is expected to be a file with three columns. The first column is the name of the departure airport,
    the second column is the name of the detination airport and the final column holds the time taken.

    :param: path: The path to the file holding the airport information
    :param: seperator: The seperator between the columns
    """
    df = pd.read_csv(path, sep = seperator)
    graph = nx.from_pandas_edgelist(df, source = "Dep", target = "Arr", edge_attr = True, create_using = nx.DiGraph())
    return graph


def read_in_airports(allowed_nodes: List[str]) -> Tuple[str, str]:
    """
    Reads from the command line the airports to get the shortest distance

    :param allowed_nodes: The nodes which are in the airport graph
    :return: departing airport name, destination airport name
    """
    error = None
    while True:

        if error:
            print(error)
        both_airports = input(
            "Please enter a departure airport and a destination airport in the format <DEP> -- <DES>: ")
        try:
            departing_airport, destination_airport = [a.strip() for a in both_airports.split("--")]
        except Exception as e:
            error = "Unable to parse the airports - did you only use a single dash?"
            continue
        if departing_airport not in allowed_nodes and destination_airport not in allowed_nodes:
            error = "Unable to recognise the departure airport or the destination airport"
        elif destination_airport not in allowed_nodes:
            error = f"Unable to recognise the destination airport"
        elif departing_airport not in allowed_nodes:
            error = f"Unable to recognise the departure airport"
        else:
            break
        if error:
            error = error + f" - available airports are {allowed_nodes}"
    return departing_airport, destination_airport


def get_shortest_path(graph: nx.DiGraph, departure_airport: str, destination_airport: str) -> Union[Tuple[int, list],
                                                                                                    Tuple[None, None]]:
    """
    Get the shortest path between nodes

    Handles missing nodes, and no path available
    :param graph: Graph holding the airport connection information
    :param departure_airport: The source node
    :param destination_airport: The destination node
    :return: total lenght of the path, the path taken
    """
    try:
        length, path = nx.single_source_dijkstra(graph, departure_airport, destination_airport, weight = "Time")
    except nx.exception.NetworkXNoPath:
        length, path = None, None
    except nx.NodeNotFound:
        length, path = None, None
    return length, path


def format_output(graph: nx.Graph, length: int, path: list) -> str:
    """
    Format the output

    :param graph: The graph holding the airport connection information
    :param length: The total path length
    :param path: The path used
    :return: formatted output string
    """
    try:
        output = ""
        for index, p in enumerate(path[:-1]):
            output +=f"{p} -- {path[index + 1]} ({graph[p][path[index + 1]]['Time']}) \n"
        output += f"time: {length}"
    except nx.NodeNotFound:
        output = "No path found"
    return output


def calculate_shortest_path(filename: str, seperator: str= ";") -> None:
    """
    Read in the airport information, the source airport, the destination airport and calculate the shortest path
    :param filename: File holding the airport information
    :return:
    """
    graph = read_in_graph(filename, seperator= seperator)
    departure_airport, destination_airport = read_in_airports(graph.nodes())
    length, shortest_path = get_shortest_path(graph, departure_airport, destination_airport)
    if length is None:
        print("No path fount")
    else:
        print(format_output(graph, length, shortest_path))


if __name__ == "__main__":
    args = sys.argv
    print(args)
    if len(args) > 2:
        filename = args[1]
        seperator = args[2]
    elif len(args) == 2:
        filename = args[1]
        seperator = ","
    else:
        filename = "Airports.csv"
        seperator = ";"
    calculate_shortest_path(filename, seperator)
