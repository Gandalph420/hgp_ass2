# Inspired by PyQt5 Creating Paint Application In 40 Minutes
#  https://www.youtube.com/watch?v=qEgyGyVA1ZQ

# NB If the menus do not work then click on another application ad then click back
# and they will work https://python-forum.io/Thread-Tkinter-macOS-Catalina-and-Python-menu-issue

# PyQt documentation links are prefixed with the word 'documentation' in the code below and can be accessed automatically
#  in PyCharm using the following technique https://www.jetbrains.com/help/pycharm/inline-documentation.html

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QDockWidget, QGridLayout, QSlider, QWidget, \
    QVBoxLayout, QLabel, QRadioButton, QHBoxLayout, QButtonGroup, QGroupBox, QComboBox
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QPixmap, QColor
import sys
from PyQt5.QtCore import Qt, QPoint
from Qt import QtGui


class PaintingApplication(QMainWindow):  # documentation https://doc.qt.io/qt-5/qmainwindow.html
    '''
    Painting Application class
    '''

    def __init__(self):
        super().__init__()

        # set window title
        self.setWindowTitle("Paint Application")

        # set the windows dimensions
        top = 400
        left = 400
        width = 800
        height = 600
        self.setGeometry(top, left, width, height)

        # set the icon
        # windows version
        self.setWindowIcon(
            QIcon("./icons/paint-brush.png"))  # documentation: https://doc.qt.io/qt-5/qwidget.html#windowIcon-prop
        # mac version - not yet working
        # self.setWindowIcon(QIcon(QPixmap("./icons/paint-brush.png")))

        # image settings (default)
        self.image = QImage(self.size(),
                            QImage.Format_RGB32)  # documentation: https://doc.qt.io/qt-5/qimage.html#QImage-1
        self.image.fill(Qt.white)  # documentation: https://doc.qt.io/qt-5/qimage.html#fill-1

        # draw settings (default)
        self.drawing = False
        self.brushSize = 3
        self.brushColor = Qt.black
        self.brushCapType = Qt.RoundCap
        self.brushJoinType = Qt.RoundJoin
        self.brushLineType = Qt.SolidLine  # documenation: https://doc.qt.io/qtforpython/PySide2/QtCore/Qt.html

        # reference to last point recorded by mouse
        self.lastPoint = QPoint()  # documenation: https://doc.qt.io/qt-5/qpoint.html

        # set up menus
        mainMenu = self.menuBar()  # create and a menu bar
        fileMenu = mainMenu.addMenu(
            " File")  # add the file menu to the menu bar, the space is required as "File" is reserved in Mac
        brushSizeMenu = mainMenu.addMenu(" Brush Size")  # add the "Brush Size" menu to the menu bar
        brushColorMenu = mainMenu.addMenu(" Brush Colour")  # add the "Brush Colour" menu to the menu bar

        # save menu item
        saveAction = QAction(QIcon("./icons/save.png"), "Save",
                             self)  # create a save action with a png as an icon, documenation: https://doc.qt.io/qt-5/qaction.html
        saveAction.setShortcut(
            "Ctrl+S")  # connect this save action to a keyboard shortcut, documentation: https://doc.qt.io/qt-5/qaction.html#shortcut-prop
        fileMenu.addAction(
            saveAction)  # add the save action to the file menu, documentation: https://doc.qt.io/qt-5/qwidget.html#addAction
        saveAction.triggered.connect(
            self.save)  # when the menu option is selected or the shortcut is used the save slot is triggered, documenation: https://doc.qt.io/qt-5/qaction.html#triggered

        # open menu item
        openAction = QAction(QIcon("./icons/save.png"), "Load", self)  # TODO Change ICON
        openAction.setShortcut("Ctrl+L")
        fileMenu.addAction(openAction)
        openAction.triggered.connect(self.open)

        # clear
        clearAction = QAction(QIcon("./icons/clear.png"), "Clear", self)  # create a clear action with a png as an icon
        clearAction.setShortcut("Ctrl+C")  # connect this clear action to a keyboard shortcut
        fileMenu.addAction(clearAction)  # add this action to the file menu
        clearAction.triggered.connect(
            self.clear)  # when the menu option is selected or the shortcut is used the clear slot is triggered

        # close
        closeAction = QAction(QIcon("./icons/save.png"), "Exit", self)  # TODO Change ICON
        closeAction.setShortcut("Ctrl+L")
        fileMenu.addAction(closeAction)
        closeAction.triggered.connect(self.close)

        # brush thickness
        threepxAction = QAction(QIcon("./icons/threepx.png"), "3px", self)
        threepxAction.setShortcut("Ctrl+3")  # TODO changed the control options to be numbers
        brushSizeMenu.addAction(threepxAction)  # connect the action to the function below
        threepxAction.triggered.connect(self.threepx)

        fivepxAction = QAction(QIcon("./icons/fivepx.png"), "5px", self)
        fivepxAction.setShortcut("Ctrl+5")
        brushSizeMenu.addAction(fivepxAction)
        fivepxAction.triggered.connect(self.fivepx)

        sevenpxAction = QAction(QIcon("./icons/sevenpx.png"), "7px", self)
        sevenpxAction.setShortcut("Ctrl+7")
        brushSizeMenu.addAction(sevenpxAction)
        sevenpxAction.triggered.connect(self.sevenpx)

        ninepxAction = QAction(QIcon("./icons/ninepx.png"), "9px", self)
        ninepxAction.setShortcut("Ctrl+9")
        brushSizeMenu.addAction(ninepxAction)
        ninepxAction.triggered.connect(self.ninepx)

        # brush colors
        blackAction = QAction(QIcon("./icons/black.png"), "Black", self)
        blackAction.setShortcut("Ctrl+B")
        brushColorMenu.addAction(blackAction);
        blackAction.triggered.connect(self.black)

        redAction = QAction(QIcon("./icons/red.png"), "Red", self)
        redAction.setShortcut("Ctrl+R")
        brushColorMenu.addAction(redAction);
        redAction.triggered.connect(self.red)

        greenAction = QAction(QIcon("./icons/green.png"), "Green", self)
        greenAction.setShortcut("Ctrl+G")
        brushColorMenu.addAction(greenAction);
        greenAction.triggered.connect(self.green)

        yellowAction = QAction(QIcon("./icons/yellow.png"), "Yellow", self)
        yellowAction.setShortcut("Ctrl+Y")
        brushColorMenu.addAction(yellowAction);
        yellowAction.triggered.connect(self.yellow)

        # size Slider
        lineSize = QLabel("Line size")
        self.sizeSlider = QSlider(Qt.Horizontal)
        self.sizeSlider.setMinimum(3)
        self.sizeSlider.setMaximum(9)
        self.sizeSlider.setTickInterval(2)
        self.sizeSlider.setSingleStep(2)  # TODO doesn´t seem to work with the steps
        self.sizeSlider.setTickPosition(QSlider.TicksBelow)
        self.sizeSlider.valueChanged.connect(self.sliderEvent)
        self.selectedLineSize = QLabel(str(self.sizeSlider.value()) + " px")

        # line Type RadioButton
        lineTypebuttonGroup = QButtonGroup()
        lineTypeLabel = QLabel("Line Type")

        solidLine = QRadioButton("Solid", self)
        solidLine.clicked.connect(self.solidLine)
        lineTypebuttonGroup.addButton(solidLine)
        solidLine.setChecked(True)

        dashLine = QRadioButton("Dash", self)
        dashLine.clicked.connect(self.dashLine)
        lineTypebuttonGroup.addButton(dashLine)

        dotLine = QRadioButton("Dot", self)
        dotLine.clicked.connect(self.dotLine)
        lineTypebuttonGroup.addButton(dotLine)

        dashDotLine = QRadioButton("DashDot", self)
        dashDotLine.clicked.connect(self.dashDotLine)
        lineTypebuttonGroup.addButton(dashDotLine)

        dashDotDotLine = QRadioButton("DashDotDot", self)
        dashDotDotLine.clicked.connect(self.dashDotDotLine)
        lineTypebuttonGroup.addButton(dashDotDotLine)

        lineTypeBox = QGroupBox("Line Type")
        lineTypeVBox = QVBoxLayout()
        lineTypeBox.setLayout(lineTypeVBox)
        lineTypeVBox.addWidget(solidLine)
        lineTypeVBox.addWidget(dashLine)
        lineTypeVBox.addWidget(dotLine)
        lineTypeVBox.addWidget(dashDotLine)
        lineTypeVBox.addWidget(dashDotDotLine)

        # cap Type radio button
        capTypeButtonGroup = QButtonGroup()
        capTypeLabel = QLabel("Cap Type")

        roundCapType = QRadioButton("Round", self)
        roundCapType.clicked.connect(self.roundCapType)
        capTypeButtonGroup.addButton(roundCapType)
        roundCapType.setChecked(True)

        flatCapType = QRadioButton("Flat", self)
        flatCapType.clicked.connect(self.flatCapType)
        capTypeButtonGroup.addButton(flatCapType)

        squareCapType = QRadioButton("Square", self)
        squareCapType.clicked.connect(self.squareCapType)
        capTypeButtonGroup.addButton(squareCapType)

        capTypeBox = QGroupBox("Cap Type")
        capTypeVBox = QVBoxLayout()
        capTypeBox.setLayout(capTypeVBox)
        capTypeVBox.addWidget(roundCapType)
        capTypeVBox.addWidget(flatCapType)
        capTypeVBox.addWidget(squareCapType)

        # join Type radio button
        joinTypeButtonGroup = QButtonGroup()
        joinTypeLabel = QLabel("Join Type")

        roundJoinType = QRadioButton("Round", self)
        roundJoinType.clicked.connect(self.roundJoinType)
        joinTypeButtonGroup.addButton(roundJoinType)
        roundJoinType.setChecked(True)

        miterJoinType = QRadioButton("Miter", self)
        miterJoinType.clicked.connect(self.miterJoinType)
        joinTypeButtonGroup.addButton(miterJoinType)

        bevelJoinType = QRadioButton("Bevel", self)
        bevelJoinType.clicked.connect(self.bevelJoinType)
        joinTypeButtonGroup.addButton(bevelJoinType)

        joinTypeBox = QGroupBox("Join Type")
        joinTypeVBox = QVBoxLayout()
        joinTypeBox.setLayout(joinTypeVBox)
        joinTypeVBox.addWidget(roundJoinType)
        joinTypeVBox.addWidget(bevelJoinType)
        joinTypeVBox.addWidget(miterJoinType)

        # color
        colorLabel = QLabel("Color")
        self.colorCombobox = QComboBox()
        self.colorCombobox.addItem("Black")
        self.colorCombobox.addItem("Red")
        self.colorCombobox.addItem("Green")
        self.colorCombobox.addItem("Yellow")
        self.colorCombobox.currentIndexChanged.connect(self.colorComboboxEvent)

        # dock widget
        self.docked = QDockWidget("Dockwidget", self)
        self.docked.setFloating(True)
        # self.addDockWidget(Qt.LeftDockWidgetArea, self.docked)
        self.dockWidget = QWidget(self)
        self.docked.setWidget(self.dockWidget)
        self.dockWidget.setLayout(QGridLayout())

        self.dockWidget.layout().addWidget(lineSize, 0, 0)
        self.dockWidget.layout().addWidget(self.sizeSlider, 0, 1)
        self.dockWidget.layout().addWidget(self.selectedLineSize, 0, 2)

        self.dockWidget.layout().addWidget(colorLabel, 1, 0)
        self.dockWidget.layout().addWidget(self.colorCombobox, 1, 1)

        #self.dockWidget.layout().addWidget(lineTypeLabel, 2, 0)
        #self.dockWidget.layout().addWidget(solidLine, 2, 1)
        #self.dockWidget.layout().addWidget(dashLine, 2, 2)
        #self.dockWidget.layout().addWidget(dotLine, 2, 3)
        #self.dockWidget.layout().addWidget(dashDotLine, 2, 4)
        #self.dockWidget.layout().addWidget(dashDotDotLine, 2, 5)
        self.dockWidget.layout().addWidget(lineTypeBox, 2, 0)

        #self.dockWidget.layout().addWidget(capTypeLabel, 3, 0)
        #self.dockWidget.layout().addWidget(roundCapType, 3, 1)
        #self.dockWidget.layout().addWidget(flatCapType, 3, 2)
        #self.dockWidget.layout().addWidget(squareCapType, 3, 3)
        self.dockWidget.layout().addWidget(capTypeBox, 3, 0)

        #self.dockWidget.layout().addWidget(joinTypeLabel, 4, 0)
        #self.dockWidget.layout().addWidget(roundJoinType, 4, 1)
        #self.dockWidget.layout().addWidget(miterJoinType, 4, 2)
        #self.dockWidget.layout().addWidget(bevelJoinType, 4, 3)
        self.dockWidget.layout().addWidget(joinTypeBox, 3, 1)


    # event handlers
    def sliderEvent(self):
        val = self.sizeSlider.value()
        self.selectedLineSize.setText(str(val) + " px")
        if (val == 3):
            self.threepx()
        elif (val == 5):
            self.fivepx()
        elif (val == 7):
            self.sevenpx()
        elif (val == 9):
            self.ninepx()

    def colorComboboxEvent(self):
        val = self.colorCombobox.currentText()
        if (val == "Black"):
            self.black()
        elif (val == "Red"):
            self.red()
        elif (val == "Yellow"):
            self.yellow()
        elif (val == "Green"):
            self.green()

    def mousePressEvent(self,
                        event):  # when the mouse is pressed, documentation: https://doc.qt.io/qt-5/qwidget.html#mousePressEvent
        if event.button() == Qt.LeftButton:  # if the pressed button is the left button
            self.drawing = True  # enter drawing mode
            self.lastPoint = event.pos()  # save the location of the mouse press as the lastPoint
            print(self.lastPoint)  # print the lastPoint for debigging purposes

    def mouseMoveEvent(self,
                       event):  # when the mouse is moved, documenation: documentation: https://doc.qt.io/qt-5/qwidget.html#mouseMoveEvent
        if event.buttons() & Qt.LeftButton & self.drawing:  # if there was a press, and it was the left button and we are in drawing mode
            painter = QPainter(self.image)  # object which allows drawing to take place on an image
            # allows the selection of brush colour, brish size, line type, cap type, join type. Images available here http://doc.qt.io/qt-5/qpen.html
            painter.setPen(
                QPen(self.brushColor, self.brushSize, self.brushLineType, self.brushCapType, self.brushJoinType))
            painter.drawLine(self.lastPoint,
                             event.pos())  # draw a line from the point of the orginal press to the point to where the mouse was dragged to
            self.lastPoint = event.pos()  # set the last point to refer to the point we have just moved to, this helps when drawing the next line segment
            self.update()  # call the update method of the widget which calls the paintEvent of this class

    def mouseReleaseEvent(self,
                          event):  # when the mouse is released, documentation: https://doc.qt.io/qt-5/qwidget.html#mouseReleaseEvent
        if event.button == Qt.LeftButton:  # if the released button is the left button, documenation: https://doc.qt.io/qt-5/qt.html#MouseButton-enum ,
            self.drawing = False  # exit drawing mode

    # paint events
    def paintEvent(self, event):
        # you should only create and use the QPainter object in this method, it should be a local variable
        canvasPainter = QPainter(
            self)  # create a new QPainter object, documenation: https://doc.qt.io/qt-5/qpainter.html
        canvasPainter.drawImage(self.rect(), self.image,
                                self.image.rect())  # draw the image , documentation: https://doc.qt.io/qt-5/qpainter.html#drawImage-1

    # resize event - this fuction is called
    def resizeEvent(self, event):
        self.image = self.image.scaled(self.width(), self.height())

    # slots
    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                  "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)")
        if filePath == "":  # if the file path is empty
            return  # do nothing and return
        self.image.save(filePath)  # save file image to the file path

    def clear(self):
        self.image.fill(Qt.white)  # fill the image with white, documentaiton: https://doc.qt.io/qt-5/qimage.html#fill-2
        self.update()  # call the update method of the widget which calls the paintEvent of this class

    def setBrushSize(self, val):
        self.brushSize = val

    def setBrushColor(self, val):
        self.brushColor = val

    def setBrushLineType(self, val):
        self.brushLineType = val

    def setCapType(self, val):
        self.brushCapType = val

    def setJoinType(self, val):
        self.brushJoinType = val

    def threepx(self):  # the brush size is set to 3
        self.brushSize = 3

    def fivepx(self):
        self.brushSize = 5

    def sevenpx(self):
        self.brushSize = 7

    def ninepx(self):
        self.brushSize = 9

    def black(self):  # the brush color is set to black
        self.brushColor = Qt.black

    def red(self):
        self.brushColor = Qt.red

    def green(self):
        self.brushColor = Qt.green

    def yellow(self):
        self.brushColor = Qt.yellow

    def solidLine(self):
        self.brushLineType = Qt.SolidLine

    def dashLine(self):
        self.brushLineType = Qt.DashLine

    def dotLine(self):
        self.brushLineType = Qt.DotLine

    def dashDotLine(self):
        self.brushLineType = Qt.DashDotLine

    def dashDotDotLine(self):
        self.brushLineType = Qt.DashDotDotLine

    def roundCapType(self):
        self.brushCapType = Qt.RoundCap

    def flatCapType(self):
        self.brushCapType = Qt.FlatCap

    def squareCapType(self):
        self.brushCapType = Qt.SquareCap

    def roundJoinType(self):
        self.brushJoinType = Qt.RoundJoin

    def miterJoinType(self):
        self.brushJoinType = Qt.MiterJoin

    def bevelJoinType(self):
        self.brushJoinType = Qt.BevelJoin

    # open a file
    def open(self):
        '''
        This is an additional function which is not part of the tutorial. It will allow you to:
         - open a file doalog box,
         - filter the list of files according to file extension
         - set the QImage of your application (self.image) to a scaled version of the file)
         - update the widget
        '''
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Image", "",
                                                  "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)")
        if filePath == "":  # if not file is selected exit
            return
        with open(filePath, 'rb') as f:  # open the file in binary mode for reading
            content = f.read()  # read the file
        self.image.loadFromData(content)  # load the data into the file
        width = self.width()  # get the width of the current QImage in your application
        height = self.height()  # get the height of the current QImage in your application
        self.image = self.image.scaled(width, height)  # scale the image from file and put it in your QImage
        self.update()  # call the update method of the widget which calls the paintEvent of this class


# this code will be executed if it is the main module but not if the module is imported
#  https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PaintingApplication()
    window.show()
    app.exec()  # start the event loop running
