class FrameCounter(object):
    def __init__(self, clock):
        self._clock = clock
        self._old_time = int(clock())
        self._old_count = 0
        self._count = 0

    def increment(self):
        time = int(self._clock())
        self._count += 1
        if time != self._old_time:
            self._old_count = self._count
            self._count = 0
            self._old_time = time
            print "Drawing %d frame(s) per second." % self._old_count

    def get_count(self):
        return self._old_count

    count = property(get_count)
