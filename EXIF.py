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
        self.layout = w.QStackedLayout()
        widget = w.QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
        # Actions
        openAction = w.QAction("Open...", self)
        openAction.setStatusTip("Open an image file.")
        openAction.setShortcut(g.QKeySequence.Open)
        openAction.triggered.connect(self.openMenuDialog)
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
        editMenu.addAction("test")
        # Add actions to toolbar and menu
        for element in (toolbar, fileMenu):
            element.addAction(openAction)
        

    def openMenuDialog(self, firstStart = False):
        self.loadedImagePaths, _ = w.QFileDialog.getOpenFileNames(parent=self, caption="Select one or more JPEG files to open:", filter="JPEG Image(*.jpg *.jpeg)", options=w.QFileDialog.DontUseNativeDialog)
        if self.loadedImagePaths:
            if firstStart:
                self.show()
            for imagePath in self.loadedImagePaths:
                image = g.QPixmap(imagePath)
                label = w.QLabel()
                label.setPixmap(image)
                self.layout.addWidget(label)
            
        elif firstStart:
            sys.exit()

a = w.QApplication([])
a.setApplicationName("EXIF Image Viewer")
ivw = ImageViewerWindow()
ivw.openMenuDialog(firstStart = True)
a.exec()