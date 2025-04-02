import rtmidi
from PageManager import PageManager
from ConfigManager import ConfigManager

class MidiController:
    def __init__(self, midi_in, midi_out, midi_virtual, page_manager, config_manager):
        self.midi_in = midi_in
        self.midi_out = midi_out
        self.midi_virtual = midi_virtual
        self.config_manager = config_manager # initialized in MidiDeviceManager
        self.page_manager = page_manager # initialized in MidiDeviceManager
        self.max_channels = 6

    def midi_callback(self, message, data=None):
        # print(f"Raw MIDI message: {message}")
        if isinstance(message, tuple):
            message = message[0]  # Extract the MIDI data (first element of the tuple)
        if isinstance(message, list) and len(message) > 0:
            if message[0] == 144:  # Note On (MIDI Note)
                self.handle_note_on(message)
            elif message[0] == 128:  # Note Off (MIDI Note)
                self.handle_note_off(message)
            elif message[0] in range(224, 233):  # Pitch Wheel Change (Faders)
                self.handle_pitch_wheel(message) # Handle pitch wheel changes (Faders)
        else:
            print("Unexpected MIDI message format.")

    def handle_note_on(self, message):
        print(message)  # Debug: Print the entire message for verification
        note_number = message[1]
        # print(note_number)  # Debug: Print the note number for verification
        velocity = message[2]
        print(velocity)  # Debug: Print the velocity for verification

        if velocity == 127:  # Button pressed
            print(f"Button {note_number} pressed.")
            # Handle fader bank and channel button presses
            try:
                if note_number == 46:  # Fader Bank Left
                    print("Calling Change Page Left")
                    self.page_manager.change_page('prev')
                elif note_number == 47:  # Fader Bank Right
                    self.page_manager.change_page('next')
                """elif note_number == 48:  # Channel Left
                    self.page_manager.change_channel('prev')
                elif note_number == 49:  # Channel Right
                    self.page_manager.change_channel('next')"""
            except Exception as e:
                print(f"An error occurred while handling note on: {e}")

    def handle_note_off(self, message):
        print(f"Note off received: {message}")
        # Handle note off actions if needed

    def handle_pitch_wheel(self, message):
        print(f"Pitch wheel change received: {message}")
        byte_1 = message[0]
        byte_2 = message[1]
        byte_3 = message[2]
        # Handle pitch wheel changes (Faders) if needed
        

    def start_listening(self):
        self.midi_in.set_callback(self.midi_callback)
        print("Started listening for MIDI messages...")
        
    def send_midi_message(self, message):
        self.midi_out.send_message(message)
        print(f"Sent MIDI message: {message}")
