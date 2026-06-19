class BPMManager:
    def __init__(self, initial_bpm=120):
        self.bpm = initial_bpm

    def set_bpm(self, bpm):
        if bpm < 40:
            bpm = 40

        if bpm > 240:
            bpm = 240

        self.bpm = bpm

    def increase(self):
        self.set_bpm(self.bpm + 1)

    def decrease(self):
        self.set_bpm(self.bpm - 1)

    def get_bpm(self):
        return self.bpm
