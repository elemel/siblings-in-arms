class FrameCounter:
    def __init__(self):
        self._frame_count = 0.0
        self._total_time = 0.0
        self.fps = 0.0
        
    def tick(self, dt):
        decay = max(1.0 - dt, 0.5)
        self._frame_count = self._frame_count * decay + 1.0
        self._total_time = self._total_time * decay + dt
        if self._total_time:
            self.fps = self._frame_count / self._total_time
