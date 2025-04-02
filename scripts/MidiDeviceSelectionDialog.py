from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QDialogButtonBox
from ConfigManager import ConfigManager

class MidiDeviceSelectionDialog(QDialog):
    def __init__(self, midi_device_manager, parent=None):
        super().__init__(parent)
        self.midi_device_manager = midi_device_manager
        self.setWindowTitle("MIDI Device Selection")

        layout = QVBoxLayout()

        # Create combo boxes
        self.midi_input_combo = QComboBox(self)
        self.midi_output_combo = QComboBox(self)
        self.midi_virtual_combo = QComboBox(self)

        self.midi_input_combo.addItems(self.midi_device_manager.midi_in_devices)
        self.midi_output_combo.addItems(self.midi_device_manager.midi_out_devices)
        self.midi_virtual_combo.addItems(self.midi_device_manager.midi_virtual_devices)

        # Preselect saved devices
        config_manager = ConfigManager()
        midi_in_device = config_manager.get_midi_in()
        midi_out_device = config_manager.get_midi_out()
        midi_virtual_device = config_manager.get_midi_virtual()

        if midi_in_device in self.midi_device_manager.midi_in_devices:
            self.midi_input_combo.setCurrentText(midi_in_device)
        if midi_out_device in self.midi_device_manager.midi_out_devices:
            self.midi_output_combo.setCurrentText(midi_out_device)
        if midi_virtual_device in self.midi_device_manager.midi_virtual_devices:
            self.midi_virtual_combo.setCurrentText(midi_virtual_device)

        self.midi_input_combo.currentIndexChanged.connect(self.on_midi_input_change)
        self.midi_output_combo.currentIndexChanged.connect(self.on_midi_output_change)
        self.midi_virtual_combo.currentIndexChanged.connect(self.on_midi_virtual_change)

        layout.addWidget(self.midi_input_combo)
        layout.addWidget(self.midi_output_combo)
        layout.addWidget(self.midi_virtual_combo)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def on_midi_input_change(self, index):
        self.midi_device_manager.set_midi_input(index)

    def on_midi_output_change(self, index):
        self.midi_device_manager.set_midi_output(index)

    def on_midi_virtual_change(self, index):
        self.midi_device_manager.set_midi_virtual(index)