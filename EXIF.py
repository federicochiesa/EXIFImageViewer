import PyQt5.QtWidgets as w
import PyQt5.QtGui as g
import PyQt5.QtCore as c
import PyQt5.QtTest as t

class ImageViewerWindow(w.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Viewer")
        extLayout = w.QVBoxLayout()
        bottomButtonsLayout = w.QHBoxLayout()
        extLayout.addLayout(bottomButtonsLayout)
        toolbar = w.QToolBar()
        self.addToolBar(toolbar)
        self.setStatusBar(w.QStatusBar(self))
        menu = self.menuBar()

        file_menu = menu.addMenu("&File")
        file_menu.addAction("test")



application = w.QApplication([])
application.setApplicationName("Test")

imgviewindow = ImageViewerWindow()
imgviewindow.show()
application.exec()