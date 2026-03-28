class Traffic:
    def __init__(self, congestion: float = 0.0):
        # congestion: 0.0 (free) → 1.0 (fully blocked)
        self.congestion = congestion
