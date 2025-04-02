import sys
from PyQt5.QtWidgets import QMainWindow, QMenu, QAction, QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
from MidiDeviceManager import MidiDeviceManager
from ConfigManager import ConfigManager
from PageManager import PageManager
from MidiDeviceSelectionDialog import MidiDeviceSelectionDialog
from ScribbleStripButton import ScribbleStripButton

class XTouchConfigApp(QMainWindow):
    def __init__(self):
        super().__init__()
        print("App is starting...")

        # Initialize config_manager (App needs to access stored midi device names)
        self.config_manager = ConfigManager()

        # Initialize midi_device_manager 
        self.midi_device_manager = MidiDeviceManager(self.config_manager)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Behringer X-Touch Configuration")
        self.setGeometry(100, 100, 1200, 818)
        self.create_menu()

        # Create a QGraphicsView to display the image
        self.graphics_view = QGraphicsView(self)
        self.graphics_view.setGeometry(0, 0, 1200, 818)

        # Create a QGraphicsScene and load the image
        self.scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.scene)

        pixmap = QPixmap("resources/xtouchImage.png")  # Replace with the path to your image
        self.image_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.image_item)

        # Add clickable buttons for scribble strips
        self.add_scribble_strip_buttons()

    def create_menu(self):
        menu_bar = self.menuBar()
        settings_menu = menu_bar.addMenu('Settings')

        midi_device_action = QAction('Select MIDI Devices', self)
        midi_device_action.triggered.connect(self.show_midi_device_dialog)
        settings_menu.addAction(midi_device_action)

    def show_midi_device_dialog(self):
        dialog = MidiDeviceSelectionDialog(self.midi_device_manager)
        dialog.exec_()

    def add_scribble_strip_buttons(self):
        # Define positions for the scribble strip buttons
        button_positions = [
            (49, 142),  
            (133, 142),
            (215, 142),
            (297, 142),
            (380, 142),
            (462, 142),
            (545, 142),
            (628, 142),
        ]

        self.scribble_buttons = []
        for i, pos in enumerate(button_positions):
            print(f"Debug: Creating button with fader_index = {i}, position = {pos}")  # Debugging line
            button = ScribbleStripButton(
                i, pos[0], pos[1], self.scene, 
                self.midi_device_manager.sysex_controller, 
                self.midi_device_manager.page_manager
            )
            self.scribble_buttons.append(button)
            print(f"Debug: Button created at position ({pos[0]}, {pos[1]}) with fader_index = {i}, Z-value = {button.zValue()}")  # Debugging line

        # Debugging: Verify all buttons are added to the scene
        for button in self.scribble_buttons:
            print(f"Debug: Button in scene with fader_index = {button.fader_index}, id = {id(button)}, Z-value = {button.zValue()}")

        # Debugging: Check items in the scene
        for item in self.scene.items():
            print(f"Debug: Item in scene = {item}, Z-value = {item.zValue()}")

    def change_page(self, direction):
        self.midi_device_manager.page_manager.change_page(direction)
        for button in self.scribble_buttons:
            button.update_scribble_strip()

    def closeEvent(self, event): # Stop the SysEx handshake thread or any background processes
        if hasattr(self.midi_device_manager, 'handshake'):
            handshake = self.midi_device_manager.handshake
            if hasattr(handshake, 'stop_handshake'):
                handshake.stop_handshake()  # Stop the SysEx handshake
                print("Handshake stopped.")
            if hasattr(handshake, 'thread') and handshake.thread.is_alive():
                handshake.thread.join()  # Ensure the thread is joined
                print("Handshake thread joined.")

        event.accept()  # Accept the event and close the application

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = XTouchConfigApp()
    window.show()
    sys.exit(app.exec_())
