import PyQt5.QtWidgets as w
import PyQt5.QtGui as g
import PyQt5.QtCore as c
import sys

class ImageViewerWindow(w.QMainWindow):
    def __init__(self):
        super().__init__()
        self.loadedImagePaths = []
        self.imageIndex = 0
        self.setWindowTitle("EXIF Image Viewer")
        # Actions
        self.openAction = w.QAction("Open...", self)
        self.openAction.setStatusTip("Open an image file.")
        self.openAction.setShortcut(g.QKeySequence.Open)
        self.openAction.triggered.connect(self.openMenuDialog)

        self.nextAction = w.QAction("Next image", self)
        self.nextAction.setStatusTip("Show the next image.")
        self.nextAction.setShortcut(g.QKeySequence.MoveToNextChar)
        self.nextAction.triggered.connect(lambda: self.changeImage(next = True))

        self.previousAction = w.QAction("Previous image", self)
        self.previousAction.setStatusTip("Show the previous image.")
        self.previousAction.setShortcut(g.QKeySequence.MoveToPreviousChar)
        self.previousAction.triggered.connect(lambda: self.changeImage(next = False))
        # Toolbar elements
        toolbar = w.QToolBar("Top toolbar")
        toolbar.setMovable(False)
        toolbar.setContextMenuPolicy(c.Qt.PreventContextMenu)
        self.addToolBar(toolbar)
        # Status bar elements
        self.setStatusBar(w.QStatusBar(self))
        # Menu bar elements
        menu = self.menuBar()
        fileMenu = menu.addMenu("&File")
        editMenu = menu.addMenu("&Edit")
        editMenu.addAction("Rotate Left")
        editMenu.addAction("Rotate Right")
        # Add actions to toolbar and menu
        for element in (toolbar, fileMenu):
            element.addAction(self.openAction)
            element.addAction(self.previousAction)
            element.addAction(self.nextAction)
    
    def changeImage(self, next):
        if next:
            self.showImageAtIndex((self.imageIndex + 1) % len(self.loadedImagePaths))
        else:
            self.showImageAtIndex((self.imageIndex - 1) % len(self.loadedImagePaths))

    def showImageAtIndex(self, index):
        image = g.QPixmap(self.loadedImagePaths[index]) # Get the first(or only) image chosen
        label = w.QLabel()
        label.setPixmap(image)
        self.setCentralWidget(label)
        self.imageIndex = index

    def openMenuDialog(self, firstStart = False):
        self.loadedImagePaths, _ = w.QFileDialog.getOpenFileNames(parent=self, caption="Select one or more JPEG files to open:", filter="JPEG Image(*.jpg *.jpeg)", options=w.QFileDialog.DontUseNativeDialog)
        if len(self.loadedImagePaths) == 1:
            self.nextAction.setEnabled(False)
            self.previousAction.setEnabled(False)
        else:
            self.nextAction.setEnabled(True)
            self.previousAction.setEnabled(True)
        if self.loadedImagePaths:
            if firstStart:
                self.show()
            self.showImageAtIndex(self.imageIndex)
        elif firstStart:
            sys.exit()

a = w.QApplication([])
a.setApplicationName("EXIF Image Viewer")
ivw = ImageViewerWindow()
ivw.openMenuDialog(firstStart = True)
a.exec()