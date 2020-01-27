#!/usr/bin/env python

"""
Day 3: Crossed Wires:
Solution to the Advent of Code calendar:
https://adventofcode.com/2019/day/3

By Adam Suhren Gustafsson (2020-01-27)
"""

import sys
import numpy as np
from itertools import combinations, product


def crossing(a, b, c, d):
    """
    Calculate crossing of line segments between points (a,b) and (c,d).
    This function assumes that one of these line segments is vertical and 
    the other horizontal.

    Args:
        a: Array on the form [x, y]
        b: Array on the form [x, y]
        c: Array on the form [x, y]
        d: Array on the form [x, y]

    Returns:
        The intersection point [x, y] of the line segments if it exists.
        None otherwise.
    """
    # (a, b) is vertical, (c, nd) is horizontal
    if a[0] == b[0] and c[1] == d[1]:
        if (min(a[1], b[1]) <= c[1] and c[1] <= max(a[1], b[1]) and 
            min(c[0], d[0]) <= a[0] and a[0] <= max(c[0], d[0])):
            return np.array([a[0], c[1]])
    # (a, b) is horizontal, (c, nd) is vertical
    if a[1] == b[1] and c[0] == d[0]:
        if (min(a[0], b[0]) <= c[0] and c[0] <= max(a[0], b[0]) and 
            min(c[1], d[1]) <= a[1] and a[1] <= max(c[1], d[1])):
            return np.array([c[0], a[1]])


def main():
    """
    Given a list of strings describing the wires of the circuit, find the
    crossings with the lowest 'central mahnattan distance' and 'wire distance'.
    """

    #wires = ['R8,U5,L5,D3', 'U7,R6,D4,L4']
    with open('input.txt', 'r') as f:
        wires = f.readlines()

    # Lookup dictionary converting 'direction codes' to vectors
    dirs = {'R' : [1, 0], 'L' : [-1, 0], 'U' : [0, 1], 'D' : [0, -1]}
    # List containing the nodes (corners) of the circuits for the wires
    nodes = []
    # List containing the 'wire distance' from the center for each node
    dists = []

    for wire in wires:
        nodes.append([np.array([0, 0])])
        dists.append([0])
        for code in wire.split(','):
            direction = code[0]
            steps = int(code[1:])
            nodes[-1].append(nodes[-1][-1] + steps * np.array(dirs[direction]))
            dists[-1].append(dists[-1][-1] + steps)

    central_dists = []
    wire_dists = []
    crossings = []

    # Take the combination of the different wire pairs
    for (n1, d1), (n2, d2) in combinations(zip(nodes, dists), 2):
        # Look at each line segment between the respective nodes
        for i, j in product(range(len(n1)-1), range(len(n2)-1)):
            c = crossing(n1[i], n1[i+1], n2[j], n2[j+1])
            # If there is a crossing (which is not [0,0]), save it!
            if c is not None and np.any(c):
                crossings.append(c)
                # Save the manhattan distance from the point to the center
                central_dists.append(sum(np.abs(c)))
                # Save the wire distance from the crossing to the center.
                # We know the distance up to the last node. We also need to add
                # the last bit of distance on the crossing of the last segment
                wd = d1[i] + d2[j] + sum(np.abs(c - n1[i]) + np.abs(c - n2[j]))
                wire_dists.append(wd)

    # Find which crossing results in the lowest distance metric
    i = np.argmin(central_dists)
    print(f'Min. central distance of {central_dists[i]} at {crossings[i]}')
    j = np.argmin(wire_dists)
    print(f'Min. wire distance of {wire_dists[j]} at {crossings[j]}')


if __name__ == '__main__':
    main()