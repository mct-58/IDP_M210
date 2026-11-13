MONDAY = [
    ('follow', 1, 'left'),   # along the front line to the bottom-right corner
    ('turn', 'left'),        # up the right edge line
    ('follow', N, 'left'),   # N = 2 loading-area stubs + bays up to the chosen one
    ('turn', 'left'),        # into the bay
    ('toEnd',),
    ('wait', 1000),          # "pickup"
    ('spin', 'left'),        # 180°
    ('follow', 1, 'both'),   # back out to the edge line (a T, so both sides)
    ('turn', 'right'),       # down the edge line
    ('follow', M, 'right'),  # M = bays below the chosen one + 1 (loading area 4)
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