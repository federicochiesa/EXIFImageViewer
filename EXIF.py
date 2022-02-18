import PyQt5.QtWidgets as w
import PyQt5.QtGui as g
import PyQt5.QtCore as c
import PyQt5.QtTest as t

class ImageViewerWindow(w.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Viewer")


application = w.QApplication([])
imgviewindow = ImageViewerWindow()
imgviewindow.show()
application.exec()