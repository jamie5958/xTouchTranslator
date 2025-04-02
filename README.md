This is a Python application that manages communication between a Behringer XTouch Universal Control Surface and a DAW like software.
I am building this specifically for QLab, but it may work in other software given the design.

This build is a proof of concept. The only thing working at this moment is writing to the scribble strips and having 14 pages of faders.
  Click the white buttons on top of the scribble strips to set text and color.
  Press the FADER BANK buttons on the physical XTouch to navigate the fader pages.

If you want to test this yourself, change the midi_in and midi_out in config.json to your appropriate midi interface.
It is prefilled with 
    "midi_in": "USB MIDI Interface 2",
    "midi_out": "USB MIDI Interface 3",
    "midi_virtual": "loopMIDI Port 2",...

These are for my setup specifically. I am using a USB MIDI interface with the MIDI ports on the XTouch.
midi_virtual is a placeholder for the software. It has no function currently, so set it to any MIDI output other than the ones used for the XTouch.

Run config_app.py from a terminal inside the virtual environment (I used the terminal in Visual Studio Code) !! I only tested this on Windows currently, but I will be testing this on Mac soon !!:
  Navigate to the project directory using "cd" (Windows); or "dir" (Mac)
  Activate the virtual environment: .\venv\Scripts\activate (Windows); source ./venv/Scripts/activate (Mac)
  Run config_app.py: python .\scripts\config_app.py (Windows); python3 ./scripts/config_app.py

!! Note !!
This only works with the XTouch in Xctl MIDI mode. 
  Press and hold the channel one select button while pressing the power button. Continue holding the select button until you see "Mode" on scribble 1 and "Ifc" on scribble 2. 
  Rotate the channel 1 encoder knob (Directly above the screen that says "Mode") until you see "Xctl"
  Rotate the channel 2 encoder knob (Directly above the screen that says "Ifc") until you see "MIDI"
  Press the channel 1 select button (It is lit green) once to exit the configuration

Let me know if you encounter any issues with either platform!
More to come soon!
