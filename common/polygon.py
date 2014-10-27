import numpy as np
import itertools

import bisect

def orient_up(p1, p2):
    """ Orient the line so that the first point has smaller y value [1] """
    if p1[1] > p2[1]:
        return p2, p1
    else:
        return p1, p2

def line_intersect_y(line, y):
    if y < line[0][1] or y > line[1][1]:    # if we are completely out of interval
        return 0, False
    if y == line[0][1]:                     # two lines meet at endpoints,
        return 0, False                     # consider only one that ends here, not one that starts
    dx = line[1][0] - line[0][0]
    dy = line[1][1] - line[0][1]
    
    return line[0][0] + int(float(y - line[0][1])/dy*dx) , True

def get_intersection_points(active_edge, y):
    intersections = []
    for edge in active_edge:
        pt, ok = line_intersect_y ( edge[2], y )
        if ok:
            bisect.insort(intersections, pt)
    return intersections

def edge_y_ordered (edge):
    """ Retur ymin, ymax, flipped"""
    if edge[0][1] > edge[1][1]:
        return edge[1][1], edge[0][1], True
    else:
        return edge[0][1], edge[1][1], False

def add_entering_edges(active_edges, edges, edge_idx, y):
    last_added = len(edges)
    print "Checking edge: ", edges[0], y
    while edge_idx < len(edges): # also stop when ymin goes above y
        e = edges[edge_idx]
        edge_idx += 1
        ymin, ymax, flipped = edge_y_ordered(e)
        if y == ymin: # enter on ymin (top is included)
            if ymax == y: # edge is starting and ending on same scanline. Skip it
                continue
            xmin = min(e[0][0], e[1][0])
            active_edges.append( (ymax, xmin, e) )    # add slope instead of edge
            last_added = edge_idx - 1
            print "appending edge, idx, y: ", active_edges[-1], edge_idx, y
        if edge_idx<len(edges):
            print "Checking edge: ", edges[edge_idx], y
    # use bisect here, but for now:
    active_edges.sort(lambda l1, l2: int(l1[1] - l2[1]))      # sort active edges by xmin
    #maybe not even sort these, but just intersection pts
    return last_added

def remove_leaving_edges(active_edge, y):
    for i in xrange(len(active_edge)-1, -1, -1): # from last edge to first
        if y > active_edge[i][0]:    # y > ymax, leave the bottom pixel
            print "removing edge, y: ", active_edge[i], y
            del active_edge[i]

def draw_convex_polygon(img, points, val):
    # Create list of edges from points [ (p0, p1), (p1, p2), ... , (pn-1, p0) ]
    edge = [orient_up(a,b) for (a, b) in itertools.izip_longest(points, points[1:], fillvalue=points[0])]
    
    print edge
    
    edge.sort(lambda l1, l2: int(min(l1[0][1],l1[1][1]) - min(l2[0][1],l2[1][1]) ) )    # sort by smaller y. We now have some redundancy. Maybe eliminate flipping of the edges. Not the fastest way to sort with comparison like this

    active_edge = []
    edge_idx = 0 # edges up to here are being processed
    for y in xrange(edge[0][0][1], edge[-1][1][1]+1): # from the smallest  to largest y in any edge
        print "Y: ", y
        edge_idx = add_entering_edges(active_edge,edge, edge_idx, y)
        remove_leaving_edges(active_edge, y)
        print "Y: %s considering edges: %s" % (y, str(active_edge))
        intersections = get_intersection_points(active_edge, y)
        print "Intersections at y: ", intersections
        for i, pt in enumerate(intersections):
            if i%2 == 0:   # they should always come in pairs
                print "I'm drawing a line: (%s, %s) - (%s, %s)" % (pt, y, intersections[i+1], y)
                img[y][pt:intersections[i+1]] = val  # fill the scanline part
                
    print "Finished: edges: ", active_edge
