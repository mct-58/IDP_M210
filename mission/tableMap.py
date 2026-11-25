# Table map: every line the robot can drive on, as a graph.
#
# Nodes are named places (junctions, line ends, depot boxes, bay ends).
# Each edge is written ONCE as (fromNode, toNode, heading, lengthMm, drivable);
# the reverse direction is implied (same length, opposite heading) and is built
# by the code that reads this file.
#
# Headings: N points from the start box towards the racks.
# drivable = False: the line exists (so junctions are labelled correctly for
# counting) but routes must never use it (the start box outline).
#
# Naming:
#   Start      centre line meets the front line (robot starts here)
#   StartBF    centre line crosses the start box front edge
#   StartBL/BR box sides cross the front line; StartBFL/BFR, StartBLB/BRB box corners
#   LC, RC     front corners
#   RD1, RD2   right depot junctions on the edge line (1 = nearer the front);
#              RD11, RD21 = the depot box ends. Left side: LD...
#   RB1..RB6   right lower-rack bay junctions (1 = nearest the depots);
#              RB11..RB61 = bay ends; RBE = top end of the edge line. Left: LB...
#   FB1..FB6   deck centre-line junctions (1 = nearest the ramp); FBE = end
#   FBkL, FBkR deck bay ends, upper left / upper right rack

N = 0
E = 1
S = 2
W = 3

# --------------------------------------------------- LENGTHS (mm) ----------
# Measured on the table, 25 Nov 2026 (right half). Centre of tape to centre
# of tape; line ends to the end of the tape. The route translator uses these
# to decide which junctions are already behind the sensors after a turn, so
# re-measure if the table or the robot's sensor position changes.
FRONT_SIDE_MM      = 830   # start box side -> front corner
BOX_HALF_MM        = 170   # centre line -> start box side
BOX_FRONT_MM       = 170   # front line -> start box front edge
BOX_BACK_MM        = 160   # front line -> start box back edge
TO_DECK_MM         = 1350   # StartBF -> first deck junction, incl. ramp
DECK_SPACING_MM    = 100   # between deck junctions
DECK_END_MM        = 125   # last deck junction -> end of deck line
DECK_STUB_MM       = 365   # deck junction -> upper bay end
CORNER_TO_DEPOT_MM = 610   # front corner -> first depot junction
DEPOT_SPACING_MM   = 300   # between the two depot junctions
DEPOT_TO_BAY_MM    = 590   # second depot junction -> first bay junction
BAY_SPACING_MM     = 95   # between lower bay junctions
EDGE_END_MM        = 120   # last bay junction -> top end of edge line
DEPOT_STUB_MM      = 190   # edge line -> depot box
BAY_STUB_MM        = 480   # edge line -> lower bay end

BAYS_PER_RACK = 6
DEPOTS_PER_SIDE = 2

# ------------------------------------------------------------ EDGES --------
EDGES = []

# Front line, west to east
EDGES.append(('LC', 'StartBL', E, FRONT_SIDE_MM, True))
EDGES.append(('StartBL', 'Start', E, BOX_HALF_MM, True))
EDGES.append(('Start', 'StartBR', E, BOX_HALF_MM, True))
EDGES.append(('StartBR', 'RC', E, FRONT_SIDE_MM, True))

# Start box outline: present for junction labelling only, never driven
EDGES.append(('StartBF', 'StartBFL', W, BOX_HALF_MM, False))
EDGES.append(('StartBF', 'StartBFR', E, BOX_HALF_MM, False))
EDGES.append(('StartBFL', 'StartBL', S, BOX_FRONT_MM, False))
EDGES.append(('StartBFR', 'StartBR', S, BOX_FRONT_MM, False))
EDGES.append(('StartBL', 'StartBLB', S, BOX_BACK_MM, False))
EDGES.append(('StartBR', 'StartBRB', S, BOX_BACK_MM, False))
EDGES.append(('StartBLB', 'StartBRB', E, 2 * BOX_HALF_MM, False))

# Centre line and deck spine
EDGES.append(('Start', 'StartBF', N, BOX_FRONT_MM, True))
EDGES.append(('StartBF', 'FB1', N, TO_DECK_MM, True))
for k in range(1, BAYS_PER_RACK):
    EDGES.append(('FB' + str(k), 'FB' + str(k + 1), N, DECK_SPACING_MM, True))
EDGES.append(('FB' + str(BAYS_PER_RACK), 'FBE', N, DECK_END_MM, True))

# Deck bays (upper racks)
for k in range(1, BAYS_PER_RACK + 1):
    EDGES.append(('FB' + str(k), 'FB' + str(k) + 'L', W, DECK_STUB_MM, True))
    EDGES.append(('FB' + str(k), 'FB' + str(k) + 'R', E, DECK_STUB_MM, True))


# Edge lines, depots and lower bays. side 'R': corner RC, stubs head W.
# side 'L': corner LC, stubs head E.
def addSide(side, stubHeading):
    corner = side + 'C'
    depot = side + 'D'
    bay = side + 'B'

    EDGES.append((corner, depot + '1', N, CORNER_TO_DEPOT_MM, True))
    for k in range(1, DEPOTS_PER_SIDE):
        EDGES.append((depot + str(k), depot + str(k + 1), N, DEPOT_SPACING_MM, True))
    EDGES.append((depot + str(DEPOTS_PER_SIDE), bay + '1', N, DEPOT_TO_BAY_MM, True))
    for k in range(1, BAYS_PER_RACK):
        EDGES.append((bay + str(k), bay + str(k + 1), N, BAY_SPACING_MM, True))
    EDGES.append((bay + str(BAYS_PER_RACK), bay + 'E', N, EDGE_END_MM, True))

    for k in range(1, DEPOTS_PER_SIDE + 1):
        EDGES.append((depot + str(k), depot + str(k) + '1', stubHeading, DEPOT_STUB_MM, True))
    for k in range(1, BAYS_PER_RACK + 1):
        EDGES.append((bay + str(k), bay + str(k) + '1', stubHeading, BAY_STUB_MM, True))


addSide('R', W)
addSide('L', E)

# ------------------------------------------------- NAMED PLACES ------------
# What the Mission layer refers to. Lists are in search order (bay 1 first).
START = 'Start'

BAYS = {
    'lowerLeft': ['LB' + str(k) + '1' for k in range(1, BAYS_PER_RACK + 1)],
    'lowerRight': ['RB' + str(k) + '1' for k in range(1, BAYS_PER_RACK + 1)],
    'upperLeft': ['FB' + str(k) + 'L' for k in range(1, BAYS_PER_RACK + 1)],
    'upperRight': ['FB' + str(k) + 'R' for k in range(1, BAYS_PER_RACK + 1)],
}

# North -> left (red) depots, south -> right (green) depots
DEPOTS = {
    'north': ['LD' + str(k) + '1' for k in range(1, DEPOTS_PER_SIDE + 1)],
    'south': ['RD' + str(k) + '1' for k in range(1, DEPOTS_PER_SIDE + 1)],
}

UPPER_LAYERS = ('upperLeft', 'upperRight')