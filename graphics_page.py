from PySide6.QtWidgets import (QGraphicsView, QGraphicsScene, QGraphicsTextItem,
    QGraphicsEllipseItem)
from PySide6.QtGui import QBrush, QFont, QImage, QTextCursor, QTextBlockFormat
from PySide6.QtCore import Qt


class Stimulus(QGraphicsEllipseItem):
    def move(self, x, y):
        self.setPos(x, y)

class Graphics_Page(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.graphics_scene = QGraphicsScene(self)
        self.setScene(self.graphics_scene)

        self.fixation = Stimulus()
        self.target = Stimulus()

        self.title = QGraphicsTextItem("")
        self.instructions = QGraphicsTextItem("")

        self.graphics_scene.addItem(self.fixation)
        self.fixation.hide()

        self.graphics_scene.addItem(self.target)
        self.target.hide()

        self.graphics_scene.addItem(self.instructions)
        self.graphics_scene.addItem(self.title)

    def apply_ui_properties(self):
        """Apply the Designer properties to items that are drawn in the scene."""
        self.graphics_scene.setSceneRect(self.sceneRect())
        self.centerOn(0, 0)  # CONFIG: Center the view on the scene origin; scene units are not visual degrees.

        diameter = self._design_property("stimulusDiameter")  # CONFIG: Read the shared dot diameter from mainwindow.ui.
        for stimulus, color_name in (
            (self.fixation, "fixationColor"),
            (self.target, "targetColor"),
        ):
            stimulus.setRect(-diameter / 2, -diameter / 2, diameter, diameter)  # CONFIG: Set dot size and center; configure each dot here for different sizes.
            stimulus.setBrush(QBrush(self._design_property(color_name)))  # CONFIG: Read dot fill colors from the UI fixationColor and targetColor properties.

        # The original module-level fonts used Qt's pre-QApplication DPI.
        # Keep their rendered size while reading font choices from the form.
        font_device = QImage(1, 1, QImage.Format.Format_ARGB32)
        dots_per_meter = round(self._design_property("sceneTextDpi") / 0.0254)
        font_device.setDotsPerMeterX(dots_per_meter)
        font_device.setDotsPerMeterY(dots_per_meter)

        self.title.setFont(QFont(self._design_property("titleFont"), font_device))  # CONFIG: Read the title font and size from the UI titleFont property.
        self.title.setDefaultTextColor(self._design_property("titleColor"))  # CONFIG: Read the title color from the UI titleColor property.
        self.instructions.setFont(QFont(self._design_property("instructionsFont"), font_device))  # CONFIG: Read the instruction font and size from the UI instructionsFont property.
        self.instructions.setDefaultTextColor(self._design_property("instructionsColor"))  # CONFIG: Read the instruction color from the UI instructionsColor property.
        self.instructions.setTextWidth(self._design_property("instructionsWidth"))  # CONFIG: Read the instruction wrapping width from the UI instructionsWidth property.

    def _design_property(self, name):
        value = self.property(name)
        if value is None:
            raise RuntimeError(f"mainwindow.ui: graphics is missing property '{name}'.")
        return value

    def show_title(self, text):
        self.instructions.hide()

        self.title.setPlainText(text)

        rect = self.title.boundingRect()
        self.title.setPos(  # CONFIG: Calculate the title position.
            -rect.width() / 2,  # CONFIG: Center the title horizontally; positive offsets move right/down, negative offsets left/up.
            -rect.height() / 2  # CONFIG: Center the title vertically; positive offsets move right/down, negative offsets left/up.
        )

        self.title.show()    

    def show_instruction(self, text):
        self.title.hide()

        self.instructions.setPlainText(text)

        cursor = self.instructions.textCursor()
        block_format = QTextBlockFormat()
        block_format.setAlignment(Qt.AlignmentFlag.AlignCenter)  # CONFIG: Center instruction paragraphs; use AlignLeft or AlignRight for other alignments.

        cursor.select(QTextCursor.SelectionType.Document)
        cursor.mergeBlockFormat(block_format)

        self.instructions.setTextCursor(cursor)

        rect = self.instructions.boundingRect()
        self.instructions.setPos(  # CONFIG: Calculate the instruction position.
            -rect.width() / 2,  # CONFIG: Center instructions horizontally; positive offsets move right/down, negative offsets left/up.
            -rect.height() / 2  # CONFIG: Center instructions vertically; positive offsets move right/down, negative offsets left/up.
        )

        self.instructions.show()

    def clear_text(self):
        self.title.hide()
        self.instructions.hide()
