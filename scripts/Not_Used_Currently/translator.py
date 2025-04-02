import scripts.MidiController as MidiController
import scripts.Not_Used_Currently.osc_controller as osc_controller

def translate_midi_to_osc():
    midi_in = MidiController.open_midi_input()
    midi_out = MidiController.open_midi_output()
    osc_client = osc_controller.create_osc_client("192.168.1.100", 53000)

    while True:
        message = midi_in.get_message()
        if message:
            # Translate MIDI message to OSC message here
            osc_controller.send_osc_message(osc_client, "/some/osc/address", message[0][0])

if __name__ == "__main__":
    translate_midi_to_osc()
