MONDAY = [
    ('follow', 1, 'left'),   # along the front line to the bottom-right corner
    ('turn', 'left'),        # up the right edge line
    ('follow', 5, 'left'),   # N = 2 loading-area stubs + bays up to the chosen one
    ('turn', 'left'),        # into the bay
    ('toEnd',),
    ('wait', 1000),          # "pickup"
    ('spin', 'left'),        # 180°
    ('follow', 1, 'both'),   # back out to the edge line (a T, so both sides)
    ('turn', 'right'),       # down the edge line
    ('follow', 6, 'right'),  # M = bays below the chosen one + 1 (loading area 4)
    ('turn', 'right'),       # into loading area 4
    ('toEnd',),
    ('wait', 1000),          # "unload"
    ('spin', 'right'),
    ('follow', 1, 'both'),   # back to the edge line
    ('turn', 'right'),       # down again
    ('follow', 2, 'right'),  # past loading area 3, then the corner
    ('turn', 'right'),       # onto the front line, heading left
    ('follow', 1, 'right'),  # the centre line meeting the front line at the box
    ('drive', 400, 40),      # into the box
]

PERFORM = [
    ('follow', 1, 'left'),    # 1  start box -> east along front line to bottom-right corner
    ('turn', 'left'),         # 2  north up the right edge line
    ('follow', 5, 'left'),    # 3  lower green, upper green, bay 1, bay 2, bay 3
    ('turn', 'left'),         # 4  west into bay 3
    ('toEnd',),               # 5  stop at the end of the bay line
    ('wait', 2000),           # 6  simulated pickup
    ('spin', 'left'),         # 7  180 deg, now facing east
    ('follow', 1, 'any'),     # 8  back out to the edge line
    ('turn', 'right'),        # 9  south down the edge line
    ('follow', 3, 'right'),   # 10 bay 2, bay 1, upper green, lower green
    ('turn', 'right'),        # 11 west into the lower green loading area
    ('toEnd',),               # 12 stop just inside the loading area
    ('wait', 2000),           # 13 simulated unloading
    ('drive', 720, -40),      # 14 reverse: axle back over the edge line (calibrate)
    ('pivot', 'left'),        # 15 90 deg on the spot, west -> south
    ('follow', 2, 'right'),   # 16 bottom-right corner
    ('turn', 'right'),        # 17 west along the front line
    ('follow', 1, 'right'),   # 18 centre line joining the front line, inside the box
    ('drive', 700, 40),       # 19 park inside the box (calibrate)
]

FOLLOW_ONLY = [('follow', 99, 'any')]                                    # follows until the backstop

COUNT_LEFT  = [('follow', 99, 'left')]                                   # prints the left-junction count as it drives

TURN_TEST   = [('follow', 1, 'any'), ('turn', 'left'), ('follow', 99, 'any')]

SPIN_TEST   = [('spin', 'left'), ('follow', 99, 'any')]

END_TEST    = [('toEnd',)]                                               # start on a stub, stops at the end

SPEED_TEST = [('drive', 2000, 50)]