from PyQt5.QtWidgets import QDialog, QGridLayout, QComboBox, QDialogButtonBox, QLabel
from ConfigManager import ConfigManager

class MidiDeviceSelectionDialog(QDialog):
    def __init__(self, midi_device_manager, parent=None):
        super().__init__(parent)
        self.midi_device_manager = midi_device_manager
        self.setWindowTitle("MIDI Device Selection")

        layout = QGridLayout()  # Use QGridLayout for better control over positioning

        # Create labels and combo boxes
        label1 = QLabel("Select MIDI Input (MIDI Out on XTouch):", self)
        self.midi_input_combo = QComboBox(self)
        self.midi_input_combo.addItems(self.midi_device_manager.midi_in_devices)

        label2 = QLabel("Select MIDI Output (MIDI In on XTouch):", self)
        self.midi_output_combo = QComboBox(self)
        self.midi_output_combo.addItems(self.midi_device_manager.midi_out_devices)

        label3 = QLabel("Select MIDI Virtual Output (Software/DAW):", self)
        self.midi_virtual_combo = QComboBox(self)
        self.midi_virtual_combo.addItems(self.midi_device_manager.midi_virtual_devices)

        # Add labels and combo boxes to the grid layout
        layout.addWidget(label1, 0, 0)  # Row 0, Column 0
        layout.addWidget(self.midi_input_combo, 0, 1)  # Row 0, Column 1

        layout.addWidget(label2, 1, 0)  # Row 1, Column 0
        layout.addWidget(self.midi_output_combo, 1, 1)  # Row 1, Column 1

        layout.addWidget(label3, 2, 0)  # Row 2, Column 0
        layout.addWidget(self.midi_virtual_combo, 2, 1)  # Row 2, Column 1

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

        # Add dialog buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons, 3, 0, 1, 2)  # Span across 2 columns

        self.setLayout(layout)

    def on_midi_input_change(self, index):
        self.midi_device_manager.set_midi_input(index)

    def on_midi_output_change(self, index):
        self.midi_device_manager.set_midi_output(index)

    def on_midi_virtual_change(self, index):
        self.midi_device_manager.set_midi_virtual(index)