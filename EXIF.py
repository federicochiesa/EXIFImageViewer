import PyQt5.QtWidgets as w
import PyQt5.QtGui as g
import PyQt5.QtCore as c
import PyQt5.QtTest as t

class ImageViewerWindow(w.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EXIF Image Viewer")
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

        for element in (toolbar, fileMenu): # add actions to toolbar and menu
            element.addAction(openAction)

    def openMenuDialog(self):
        options = w.QFileDialog.Options()
        files, _ = w.QFileDialog.getOpenFileNames(self, "", "", "JPEG Image(*.jpg *.jpeg)", options=options)
        if files:
            print(files)

a = w.QApplication([])
a.setApplicationName("EXIF Image Viewer")
ivw = ImageViewerWindow()
ivw.show()
a.exec()