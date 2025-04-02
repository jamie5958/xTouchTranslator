class Fader:
    def __init__(self, fader_id, midi_control):
        self.fader_id = fader_id  # A unique ID for the fader
        self.midi_control = midi_control  # MIDI control change for the fader

    def set_midi_control(self, control):
        self.midi_control = control