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
        self.centerOn(0, 0)  # 《《《《《《《《《《《视图对准场景原点；场景坐标不是视角度数

        diameter = self._design_property("stimulusDiameter")  # 《《《《《《《《《《《圆点共用直径读取自mainwindow.ui
        for stimulus, color_name in (
            (self.fixation, "fixationColor"),
            (self.target, "targetColor"),
        ):
            stimulus.setRect(-diameter / 2, -diameter / 2, diameter, diameter)  # 《《《《《《《《《《《圆点尺寸及中心坐标；若需两个点不同尺寸可在此分别设置
            stimulus.setBrush(QBrush(self._design_property(color_name)))  # 《《《《《《《《《《《圆点填充色读取自UI的fixationColor和targetColor

        # The original module-level fonts used Qt's pre-QApplication DPI.
        # Keep their rendered size while reading font choices from the form.
        font_device = QImage(1, 1, QImage.Format.Format_ARGB32)
        dots_per_meter = round(self._design_property("sceneTextDpi") / 0.0254)
        font_device.setDotsPerMeterX(dots_per_meter)
        font_device.setDotsPerMeterY(dots_per_meter)

        self.title.setFont(QFont(self._design_property("titleFont"), font_device))  # 《《《《《《《《《《《标题字体字号读取自UI的titleFont
        self.title.setDefaultTextColor(self._design_property("titleColor"))  # 《《《《《《《《《《《标题颜色读取自UI的titleColor
        self.instructions.setFont(QFont(self._design_property("instructionsFont"), font_device))  # 《《《《《《《《《《《提示语字体字号读取自UI的instructionsFont
        self.instructions.setDefaultTextColor(self._design_property("instructionsColor"))  # 《《《《《《《《《《《提示语颜色读取自UI的instructionsColor
        self.instructions.setTextWidth(self._design_property("instructionsWidth"))  # 《《《《《《《《《《《提示语换行宽度读取自UI的instructionsWidth

    def _design_property(self, name):
        value = self.property(name)
        if value is None:
            raise RuntimeError(f"mainwindow.ui: graphics is missing property '{name}'.")
        return value

    def show_title(self, text):
        self.instructions.hide()

        self.title.setPlainText(text)

        rect = self.title.boundingRect()
        self.title.setPos(  # 《《《《《《《《《《《标题位置计算入口
            -rect.width() / 2,  # 《《《《《《《《《《《标题水平x居中坐标；加偏移向右／向下，减偏移向左／向上
            -rect.height() / 2  # 《《《《《《《《《《《标题垂直y居中坐标；加偏移向右／向下，减偏移向左／向上
        )

        self.title.show()    

    def show_instruction(self, text):
        self.title.hide()

        self.instructions.setPlainText(text)

        cursor = self.instructions.textCursor()
        block_format = QTextBlockFormat()
        block_format.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 《《《《《《《《《《《提示语段落居中，可改为AlignLeft或AlignRight

        cursor.select(QTextCursor.SelectionType.Document)
        cursor.mergeBlockFormat(block_format)

        self.instructions.setTextCursor(cursor)

        rect = self.instructions.boundingRect()
        self.instructions.setPos(  # 《《《《《《《《《《《提示语位置计算入口
            -rect.width() / 2,  # 《《《《《《《《《《《提示语水平x居中坐标；加偏移向右／向下，减偏移向左／向上
            -rect.height() / 2  # 《《《《《《《《《《《提示语垂直y居中坐标；加偏移向右／向下，减偏移向左／向上
        )

        self.instructions.show()

    def clear_text(self):
        self.title.hide()
        self.instructions.hide()
