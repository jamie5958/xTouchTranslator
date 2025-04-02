from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsSceneMouseEvent, QInputDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainterPath

class ScribbleStripButton(QGraphicsRectItem):
    def __init__(self, fader_index, x, y, scene, sysex_controller, page_manager):
        super().__init__(x, y, 50, 20)  # Adjust size and position as needed
        self.fader_index = fader_index
        print(f"Debug: Initializing ScribbleStripButton with fader_index = {self.fader_index}")  # Debugging line
        self.page_manager = page_manager
        self.sysex_controller = sysex_controller
        self.setBrush(Qt.lightGray)
        self.setFlag(QGraphicsRectItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsRectItem.ItemIsFocusable, True)  # Enable focusable
        self.setAcceptedMouseButtons(Qt.LeftButton)  # Ensure the button explicitly accepts left mouse clicks
        self.setZValue(10 + fader_index)  # Assign unique Z-value based on fader_index
        scene.addItem(self)

    def shape(self):
        # Define the shape of the button for hit detection
        path = QPainterPath()
        path.addRect(self.rect())
        return path

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        print(f"Debug: mousePressEvent triggered for fader_index = {self.fader_index}, button_id = {id(self)}")  # Debugging line
        item_under_mouse = self.scene().itemAt(event.scenePos(), self.scene().views()[0].transform())
        print(f"Debug: Item under mouse = {item_under_mouse}, Expected = {self}")  # Debugging line

        if item_under_mouse is not self:
            print("Debug: Event not for this button, ignoring.")  # Debugging line
            return  # Ignore the event if it's not for this button

        event.accept()  # Explicitly accept the event to prevent further propagation
        line_one_text, ok = QInputDialog.getText(None, "Configure Scribble Strip", f"Enter text for Fader {self.fader_index + 1}:")
        if ok:
            line_two_text, ok = QInputDialog.getText(None, "Configure Scribble Strip", f"Enter second line text for Fader {self.fader_index + 1}:")
            if ok:
                color, ok = QInputDialog.getItem(None, "Select Color", "Choose a color:", ["red", "green", "blue", "yellow", "pink", "cyan", "white", "off"], 0, False)
                if ok:
                    # Retrieve the current page index from the PageManager
                    page_index = self.page_manager.current_page

                    # Create the configuration dictionary
                    config = {"color": color, "line_one_text": line_one_text, "line_two_text": line_two_text}

                    # Save the configuration to the PageManager
                    self.page_manager.set_scribble_strip(self.fader_index, config)

                    # Write the configuration to the scribble strip via SysexController
                    self.sysex_controller.write_to_scribble_strip(page_index, self.fader_index, color, False, line_one_text, line_two_text)

        # Temporarily disable and re-enable the button to reset its state
        self.setEnabled(False)
        self.setEnabled(True)
        print("Debug: Button temporarily disabled and re-enabled to reset state.")

        # Clear selection and focus explicitly
        self.scene().clearSelection()  # Clear all selections in the scene
        self.clearFocus()  # Clear focus from this button
        for view in self.scene().views():
            view.clearFocus()  # Clear focus from the view
        print("Debug: Selection and focus cleared.")

    def update_scribble_strip(self):
        config = self.page_manager.get_scribble_strip(self.fader_index)
        self.sysex_controller.write_to_scribble_strip(self.fader_index, config["color"], False, config["line_one_text"], config["line_two_text"])

    def change_page(self, direction):
        self.page_manager.change_page(direction)
        # Removed reference to scribble_buttons