from utime import ticks_diff


class PackageHandler:
    def __init__(self, gripMoveMs, liftMoveMs):
        self.gripMoveMs = gripMoveMs
        self.liftMoveMs = liftMoveMs
        self.steps = None
        self.stepIndex = 0
        self.stepStart = None
        self.commandPending = False

    def start(self, action, now):
        if action not in ('pickup', 'unload'):
            raise ValueError("action must be 'pickup' or 'unload'")
        if self.steps is not None:
            raise RuntimeError('package handling is already in progress')

        if action == 'pickup':
            self.steps = (('grip', self.gripMoveMs), ('lift', self.liftMoveMs))
        else:
            self.steps = (('lower', self.liftMoveMs), ('release', self.gripMoveMs))

        self.stepIndex = 0
        self.stepStart = now
        self.commandPending = True

    def update(self, now):
        if self.steps is None:
            return ('idle', None)

        if self.commandPending:
            self.commandPending = False
            self.stepStart = now
            return ('running', self.steps[self.stepIndex][0])

        duration = self.steps[self.stepIndex][1]
        if ticks_diff(now, self.stepStart) < duration:
            return ('running', None)

        self.stepIndex += 1
        if self.stepIndex >= len(self.steps):
            self.steps = None
            self.stepStart = None
            self.commandPending = False
            return ('done', None)

        self.stepStart = now
        return ('running', self.steps[self.stepIndex][0])
