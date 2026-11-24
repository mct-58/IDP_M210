GRAB = [
    ('follow', 1, 'left'),    # 1  start box -> east along the front line to the bottom-right corner
    ('turn', 'left'),         # 2  north up the right edge line
    ('follow', 5, 'left'),    # 3  lower green, upper green, bay 1, bay 2, bay 3
    ('turn', 'left'),         # 4  west into bay 3
    ('toEnd',),               # 5  stop at the end of the bay line
    ('pickup',),              # 6  grip, then lift
    ('spin', 'left'),         # 7  180 deg, now facing east
    ('follow', 1, 'any'),     # 8  back out to the edge line
    ('turn', 'right'),        # 9  south down the edge line
    ('follow', 2, 'right'),   # 10 bay 1, upper green (bay 2 is already behind the sensors)
    ('turn', 'right'),        # 11 west into the upper green stub
    ('toBox',),               # 12 stop when the sensors reach the loading box
    ('unload',),              # 13 lower, then release
    ('drive', 590, -40),      # 14 reverse: axle back over the edge line
    ('pivot', 'left'),        # 15 90 deg on the spot, west -> south onto the edge line
    ('follow', 2, 'right'),   # 16 lower green stub, then the bottom-right corner
    ('turn', 'right'),        # 17 west along the front line
    ('follow', 1, 'right'),   # 18 centre line joining the front line, inside the box
    ('drive', 700, 40),       # 19 park inside the box
]

GRAB_LEFT = [
    ('follow', 1, 'right'),   # 1  start box -> west along the front line to the bottom-left corner
    ('turn', 'right'),        # 2  north up the left edge line
    ('follow', 5, 'right'),   # 3  lower box, upper box, bay 1, bay 2, bay 3
    ('turn', 'right'),        # 4  east into bay 3
    ('toEnd',),               # 5  stop at the end of the bay line
    ('pickup',),              # 6  grip, then lift
    ('drive', 1200, -40),      # 6b back out of the bay a little, clear of the rack, before turning
    ('spin', 'right'),        # 7  180 deg, now facing west
    ('follow', 1, 'any'),     # 8  back out to the edge line
    ('turn', 'left'),         # 9  south down the edge line
    ('follow', 2, 'left'),    # 10 bay 1, upper box (bay 2 is already behind the sensors)
    ('turn', 'left'),         # 11 east into the upper box stub
    ('toBox',),               # 12 stop when the sensors reach the loading box
    ('unload',),              # 13 lower, then release
    ('drive', 590, -40),      # 14 reverse: axle back over the edge line
    ('pivot', 'right'),       # 15 90 deg on the spot, east -> south onto the edge line
    ('follow', 2, 'left'),    # 16 lower box stub, then the bottom-left corner
    ('turn', 'left'),         # 17 east along the front line
    ('follow', 1, 'left'),    # 18 centre line joining the front line, inside the box
    ('drive', 700, 40),       # 19 park inside the box
]