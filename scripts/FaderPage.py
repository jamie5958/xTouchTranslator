class FaderPage:
    def __init__(self, page_name):
        self.page_name = page_name
        self.faders = []  # List to hold fader assignments

    def add_fader(self, fader):
        self.faders.append(fader)

    def remove_fader(self, fader):
        if fader in self.faders:
            self.faders.remove(fader)

    def get_faders(self):
        return self.faders