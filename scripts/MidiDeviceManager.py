import rtmidi
from MidiController import MidiController
from Handshake import Handshake
from ConfigManager import ConfigManager
from SysexController import SysexController
from PageManager import PageManager

class MidiDeviceManager:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.midi_in = None
        self.midi_out = None
        self.midi_virtual = None
        self.midi_in_devices = []
        self.midi_out_devices = []
        self.handshake = None
        self.midi_controller = None
        self.sysex_controller = None
        self.page_manager = None  
        
        self.init_sysex_controller()
        
        self.init_page_manager()

        self.list_midi_devices()
        self.load_saved_devices()

    

    def init_sysex_controller(self):
        if self.midi_out:
            self.sysex_controller = SysexController(self.midi_out, None)  # Initialize SysExController with MIDI Out
            print("SysExController initialized")

    def init_page_manager(self):
        if self.sysex_controller:
            self.page_manager = PageManager(self.config_manager, self.sysex_controller)
            print("PageManager initialized")

    def init_midi_controller(self):
            # Ensure all required components are set up
        if self.midi_in and self.midi_out and self.midi_virtual and self.page_manager:
            self.midi_controller = MidiController(
                self.midi_in,
                self.midi_out,
                self.midi_virtual,
                self.page_manager,  # Pass the shared PageManager
                self.config_manager  # Pass the shared ConfigManager
            )
            print("MidiController initialized.")
        else:
            print("Error: Cannot initialize MidiController. Missing required components.")

    def list_midi_devices(self):
        midi_in = rtmidi.MidiIn()
        midi_out = rtmidi.MidiOut()
        midi_virtual = rtmidi.MidiOut()
        
        # Get input and output devices
        self.midi_in_devices = midi_in.get_ports()
        self.midi_out_devices = midi_out.get_ports()
        self.midi_virtual_devices = midi_virtual.get_ports()

    def load_saved_devices(self):
        midi_in_name = self.config_manager.get_midi_in()
        midi_out_name = self.config_manager.get_midi_out()
        midi_virtual_name = self.config_manager.get_midi_virtual()
        # Check if the saved devices are still available

        if midi_in_name and midi_in_name in self.midi_in_devices:
            self.set_midi_input(self.midi_in_devices.index(midi_in_name))
            print(f"Loaded MIDI In: {midi_in_name}")
        else:
            print("No saved MIDI In device found in config.")

        if midi_out_name and midi_out_name in self.midi_out_devices:
            self.set_midi_output(self.midi_out_devices.index(midi_out_name))
            print(f"Loaded MIDI Out: {midi_out_name}")
        else:
            print("No saved MIDI Out device found in config.")
        if midi_virtual_name and midi_virtual_name in self.midi_out_devices:
            self.set_midi_virtual(self.midi_virtual_devices.index(midi_virtual_name)) 
            print(f"Loaded MIDI Virtual: {midi_virtual_name}")
        else:
            print("No saved MIDI Virtual device found in config.")

    def set_midi_input(self, device_index):
        if 0 <= device_index < len(self.midi_in_devices):
            self.midi_in = rtmidi.MidiIn()
            self.midi_in.open_port(device_index)
            print(f"Connected to MIDI In: {self.midi_in_devices[device_index]}")
            self.config_manager.save_config(midi_in = self.midi_in_devices[device_index])

            # Set up MIDI controller
            self.init_midi_controller()

    def set_midi_output(self, device_index):
        if 0 <= device_index < len(self.midi_out_devices):
            self.midi_out = rtmidi.MidiOut()
            self.midi_out.open_port(device_index)
            print(f"Connected to MIDI Out: {self.midi_out_devices[device_index]}")
            self.config_manager.save_config(midi_out=self.midi_out_devices[device_index])

            # Reinitialize SysEx Controller and PageManager
            self.init_sysex_controller()
            self.init_page_manager()
            
            # Set up MIDI controller
            self.init_midi_controller()

            if self.handshake:
                self.handshake.stop_handshake()
            self.handshake = Handshake(self.midi_out)
            self.handshake.start_handshake()

    def set_midi_virtual(self, device_index):
        if 0 <= device_index < len(self.midi_virtual_devices):
            self.midi_virtual = rtmidi.MidiOut()
            self.midi_virtual.open_port(device_index)
            print(f"Connected to MIDI Virtual: {self.midi_virtual_devices[device_index]}")
            self.config_manager.save_config(midi_virtual=self.midi_virtual_devices[device_index])

            # Reinitialize MIDI controller if all devices are ready
            self.init_midi_controller()

            # Start listening only if the MIDI controller is properly initialized
            if self.midi_controller:
                self.midi_controller.start_listening()