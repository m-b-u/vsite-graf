""" Functions related to scanline conversion of polygon to bitmap """

import itertools

import bisect

def plot_polygon(axis, p, color='b'):
    """ Plots the polygon to given pyplot axis, as regular lines.

    Argument:
      axis - pyplot axis
      p - list of points. Points can be 2-lists, 2-tuples
      color - color in pyplot string format
    """

    p2 = p[:]
    p2.append(p[0])
    # convert list of tuples to list with x coords and list with y coords
    axis.plot(*zip(*p2), color=color, marker='o', markersize=3, linestyle='-')

def orient_up(p1, p2):
    """ Orient the line so that the first point has smaller y value [1] """
    if p1[1] > p2[1]:
        return p2, p1
    else:
        return p1, p2

def line_intersect_y(line, y):
    """ Returns x coordinate of intersection between line and
    line parallel to x axis, at y

    Returns: Tuple of x coord of intersect, bool which says if we intersect"""
    if y < line[0][1] or y > line[1][1]:    # are we completely out of interval
        return 0, False
    if y == line[0][1]:                     # two lines meet at endpoints,
        return 0, False                     # consider only one that ends here,
                                            #not one that starts
    dx = line[1][0] - line[0][0]
    dy = line[1][1] - line[0][1]

    return line[0][0] + int(float(y - line[0][1])/dy*dx), True

def get_intersection_points(active_edge, y):
    """ Returns the sorted list of intersection of
    all active edges and line parallel to x axis"""
    intersections = []
    for edge in active_edge:
        pt, ok = line_intersect_y(edge[2], y)
        if ok:
            bisect.insort(intersections, pt)
    return intersections

def edge_y_ordered(edge):
    """ Return ymin, ymax, flipped"""
    if edge[0][1] > edge[1][1]:
        return edge[1][1], edge[0][1], True
    else:
        return edge[0][1], edge[1][1], False


def add_entering_edges(active_edges, edges, edge_idx, y):
    """ Adds edges to active_edges, if they enter the polygon on scanline y
    Assumes edges are sorted by smaller of y coordinates of endpoints

    Arguments:
       active_edges: list of currently active edges
       edges: list of all edges
       edge_idx: index in edged where to start checking
       y: scanline

    Returns:
      edge_idx where to continue looking next time"""
    last_added = len(edges)

    while edge_idx < len(edges):
        e = edges[edge_idx]
        ymin, ymax, flipped = edge_y_ordered(e)

        edge_idx += 1
        if ymin > y:
             # stop when ymin goes above y
            return edge_idx - 1
        if y == ymin: # enter on ymin (top is included)
            # if edge is starting and ending on same scanline. Skip it
            if ymax == y:
                continue
            xmin = min(e[0][0], e[1][0])
            active_edges.append((ymax, xmin, e))    # TODO: add slope instead of edge
            last_added = edge_idx - 1

    # sort active edges by xmin
    active_edges.sort(lambda l1, l2: int(l1[1] - l2[1]))
    # TODO: maybe not even sort these, but just intersection pts
    return last_added + 1

def remove_leaving_edges(active_edge, y):
    """ Remove the edges from active_edge if
    they are above scanline y """
    for i in xrange(len(active_edge)-1, -1, -1): # from last edge to first
        if y > active_edge[i][0]:    # y > ymax, leave the bottom pixel
            del active_edge[i]

def draw_convex_polygon(img, points, val):
    """ Draws polygon to image array using scanline conversion

    Arguments:
      img: image array
      points: list of point (x, y) tuples
      val: color value for filling
    """
    # Create list of edges from points [ (p0, p1), (p1, p2), ... , (pn-1, p0) ]
    edge = [orient_up(a, b) for (a, b)
            in itertools.izip_longest(points, points[1:], fillvalue=points[0])]
    # sort by smaller y. We are now flipping edges by y without real need.
    # Not the fastest way to sort with comparison like this
    edge.sort(lambda l1, l2: int(min(l1[0][1], l1[1][1]) -
                                 min(l2[0][1], l2[1][1])))
    active_edge = []
    edge_idx = 0 # edges up to here were processed
    # from the smallest  to largest y found in any edge
    for y in xrange(edge[0][0][1], edge[-1][1][1]+1):
        edge_idx = add_entering_edges(active_edge, edge, edge_idx, y)
        intersections = get_intersection_points(active_edge, y)
        for i, pt in enumerate(intersections):
            if i%2 == 0:   # they should always come in pairs
                img[y][pt:intersections[i+1]] = val  # fill the scanline part
        remove_leaving_edges(active_edge, y)
