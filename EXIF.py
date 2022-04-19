import PyQt5.QtWidgets as w
import PyQt5.QtGui as g
import PyQt5.QtCore as c
#import PyQt5.QtWebEngineWidgets as web
import exifread
import sys

class ImageViewerWindow(w.QMainWindow):
    def __init__(self):
        super().__init__()
        self.loadedImagePaths = []
        self.imageIndex = 0
        self.setWindowTitle("EXIF Image Viewer")
        self.scrollArea = w.QScrollArea()
        self.label = w.QLabel()
        self.setCentralWidget(self.scrollArea)
        self.scrollArea.setWidgetResizable(True)
        self.label.setAlignment(c.Qt.AlignCenter)
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

        self.EXIFAction = w.QAction("Show EXIF data", self)
        self.EXIFAction.setStatusTip("Show EXIF data for this image.")
        self.EXIFAction.setShortcut(g.QKeySequence.Italic)
        self.EXIFAction.triggered.connect(self.showEXIFWindow)

        self.RCWAction = w.QAction("Rotate Clockwise", self)
        self.RCWAction.setStatusTip("Rotate the image 90 degress clockwise.")
        self.RCWAction.setShortcut(g.QKeySequence.MoveToNextWord)
        self.RCWAction.triggered.connect(lambda: self.rotateImage(clockwise = True))

        self.RCCWAction = w.QAction("Rotate Counter-clockwise", self)
        self.RCCWAction.setStatusTip("Rotate the image 90 degress counter-clockwise.")
        self.RCCWAction.setShortcut(g.QKeySequence.MoveToPreviousWord)
        self.RCCWAction.triggered.connect(lambda: self.rotateImage(clockwise = False))

        self.zoomInAction = w.QAction("Zoom In", self)
        self.zoomInAction.setStatusTip("Scale the image by a factor of 1,25.")
        self.zoomInAction.setShortcut(g.QKeySequence.ZoomIn)
        self.zoomInAction.triggered.connect(lambda: self.scaleImage(zoomIn = True))

        self.zoomOutAction = w.QAction("Zoom Out", self)
        self.zoomOutAction.setStatusTip("Scale the image by a factor of 0,75.")
        self.zoomOutAction.setShortcut(g.QKeySequence.ZoomOut)
        self.zoomOutAction.triggered.connect(lambda: self.scaleImage(zoomIn = False))

        self.locationAction = w.QAction("Show Image Location", self)
        self.locationAction.setStatusTip("Show the image location in OpenStreetMap. (opens in a browser window)")
        self.locationAction.setShortcut(g.QKeySequence(c.Qt.CTRL + c.Qt.Key_L))
        self.locationAction.triggered.connect(self.showLocation)

        # Toolbar elements
        toolbar = w.QToolBar("Top toolbar")
        toolbar.setMovable(False)
        toolbar.setContextMenuPolicy(c.Qt.PreventContextMenu)
        self.addToolBar(toolbar)
        # Status bar declaration
        self.setStatusBar(w.QStatusBar(self))
        # Menu bar elements
        menu = self.menuBar()
        fileMenu = menu.addMenu("&File")
        editMenu = menu.addMenu("&Edit")
        # Add actions to toolbar and edit menu
        for element in (toolbar, editMenu):
            element.addAction(self.RCWAction)
            element.addAction(self.RCCWAction)
            element.addAction(self.zoomInAction)
            element.addAction(self.zoomOutAction)
        # Add actions to toolbar and file menu
        for element in (toolbar, fileMenu):
            element.addAction(self.openAction)
            element.addAction(self.previousAction)
            element.addAction(self.nextAction)
            element.addAction(self.EXIFAction)
            element.addAction(self.locationAction)

    def changeImage(self, next):
        if next:
            self.showImageAtIndex((self.imageIndex + 1) % len(self.loadedImagePaths))
        else:
            self.showImageAtIndex((self.imageIndex - 1) % len(self.loadedImagePaths))

    def topLeft(self):
        topLeftPoint = w.QDesktopWidget().availableGeometry().topLeft()
        self.move(topLeftPoint)

    def resizeWindow(self, firstTime): #resize to first image(if it fits on screen), then scale images to fit window
        imageSize = self.label.sizeHint()
        screenSize = w.QDesktopWidget().availableGeometry()
        resizeToThis = c.QSize(0,0)
        if firstTime:
            if(imageSize.width() > screenSize.width()):
                resizeToThis.setWidth(screenSize.width())
            else:
                resizeToThis.setWidth(imageSize.width())
            if(imageSize.height() > screenSize.height()):
                resizeToThis.setHeight(screenSize.height())
            else:
                resizeToThis.setHeight(imageSize.height() + 51)
            self.topLeft()
            self.resize(resizeToThis)
        if imageSize.width() > self.width() or imageSize.height() > self.height():
            self.label.setPixmap(g.QPixmap(self.loadedImagePaths[self.imageIndex]).scaled(self.width(), self.height() - 51, aspectRatioMode=c.Qt.KeepAspectRatio))
        self.label.adjustSize()

        
    def rotateImage(self, clockwise):
        if clockwise:
            self.angle = (self.angle + 90) % 360
        else:
            self.angle = (self.angle - 90) % 360
        if self.angle % 180 != 0:
            self.imageWidth = g.QPixmap(self.loadedImagePaths[self.imageIndex]).rect().height()
        else:
            self.imageWidth = g.QPixmap(self.loadedImagePaths[self.imageIndex]).rect().width()
        self.label.setPixmap(g.QPixmap(self.loadedImagePaths[self.imageIndex]).transformed(g.QTransform().rotate(self.angle), c.Qt.SmoothTransformation).scaledToWidth(int(self.imageWidth * self.scaleIndex)))
        self.label.adjustSize()
    
    def scaleImage(self, zoomIn):
        if zoomIn: 
            self.scaleIndex *= 1.25
        else:
            self.scaleIndex /= 1.25
        self.label.setPixmap(g.QPixmap(self.loadedImagePaths[self.imageIndex]).transformed(g.QTransform().rotate(self.angle), c.Qt.SmoothTransformation).scaledToWidth(int(self.imageWidth * self.scaleIndex)))

    def showImageAtIndex(self, index, firstStart = False):
        image = g.QPixmap(self.loadedImagePaths[index])
        self.label.setPixmap(image)
        self.scrollArea.setWidget(self.label)
        self.imageIndex = index
        self.angle = 0
        self.scaleIndex = 1
        self.label.adjustSize()
        self.resizeWindow(firstStart)
        self.imageWidth = image.rect().width()
        self.model = EXIFModel(self.loadedImagePaths[index])
        if self.model.getEXIFLocation() != (None, None):
            self.locationAction.setEnabled(True)
        else:
            self.locationAction.setEnabled(False)

    def openMenuDialog(self, firstStart = False):
        self.loadedImagePaths, _ = w.QFileDialog.getOpenFileNames(parent=self, caption="Select one or more JPEG files to open:", filter="JPEG Image(*.jpg *.jpeg)")
        if self.loadedImagePaths:
            if len(self.loadedImagePaths) == 1:
                self.nextAction.setEnabled(False)
                self.previousAction.setEnabled(False)
            else:
                self.nextAction.setEnabled(True)
                self.previousAction.setEnabled(True)
            if firstStart:
                self.show()
            self.imageIndex = 0
            self.showImageAtIndex(self.imageIndex, True)
        elif firstStart:
            sys.exit()
    
    def showEXIFWindow(self):
        self.exif = EXIFWindow(self.model)
        self.exif.windowClosed.connect(lambda: self.EXIFAction.setEnabled(True))
        self.exif.show()
        self.EXIFAction.setEnabled(False)

    def showLocation(self): # TODO: URL generation based on location
        coordinates = list(self.model.getEXIFLocation())
        url = "https://www.openstreetmap.org/export/embed.html?bbox=" + str(coordinates[1] - 0.5) + "," + str(coordinates[0] - 0.5) + "," + str(coordinates[1] + 0.5) + "," + str(coordinates[0] + 0.5) + "&layer=mapnik&marker=" + str(coordinates[0]) + "," + str(coordinates[1])
        self.location = LocationWindow(url)
        self.location.windowClosed.connect(lambda: self.locationAction.setEnabled(True))
        self.location.show()
        self.locationAction.setEnabled(False)

class EXIFModel(c.QAbstractTableModel):
    def __init__(self, path):
        super(EXIFModel, self).__init__()
        self.exif = self.getEXIFData(path)
        self.exifData = []
        for key, value in self.exif.items():
            self.exifData.append((key, value))

    def data(self, index, role):
        if role == c.Qt.DisplayRole:
            key, value = self.exifData[index.row()]
            if index.column() == 0:
                return key
            elif index.column() == 1:
                return str(value)
            else:
                return None
    
    def headerData(self, section, orientation, role):
        if role == c.Qt.DisplayRole:
            if orientation == c.Qt.Horizontal:
                return ["Tag ", "Value"][section]
            if orientation == c.Qt.Vertical:
                return None

    def rowCount(self, _ = None):
        return len(self.exifData)

    def columnCount(self, _ = None):
        return 2

    def getEXIFData(self, path):
        with open(path, 'rb') as f:
            EXIFTags = exifread.process_file(f)
        return EXIFTags
        
    def getIfExist(self, data, key):
        if key in data:
            return data[key]
        return None

    def convertToDegrees(self, value):
        d = float(value.values[0].num) / float(value.values[0].den)
        m = float(value.values[1].num) / float(value.values[1].den)
        s = float(value.values[2].num) / float(value.values[2].den)

        return d + (m / 60.0) + (s / 3600.0)
        
    def getEXIFLocation(self):
        latitude = None
        longitude = None

        GPSLatitude = self.getIfExist(self.exif, 'GPS GPSLatitude')
        GPSLatitudeRef = self.getIfExist(self.exif, 'GPS GPSLatitudeRef')
        GPSLongitude = self.getIfExist(self.exif, 'GPS GPSLongitude')
        GPSLongitudeRef = self.getIfExist(self.exif, 'GPS GPSLongitudeRef')

        if GPSLatitude and GPSLatitudeRef and GPSLongitude and GPSLongitudeRef:
            latitude = self.convertToDegrees(GPSLatitude)
            if GPSLatitudeRef.values[0] != 'N':
                latitude = 0 - latitude

            longitude = self.convertToDegrees(GPSLongitude)
            if GPSLongitudeRef.values[0] != 'E':
                longitude = 0 - longitude

        return latitude, longitude

class EXIFWindow(w.QMainWindow):
    windowClosed = c.pyqtSignal()

    def __init__(self, exifModel):
        super().__init__()
        self.setWindowTitle("EXIF Data")
        self.model = exifModel
        self.tableView = w.QTableView()
        self.tableView.setModel(self.model)
        self.tableView.verticalHeader().hide()
        self.setCentralWidget(self.tableView)
        self.tableView.resizeColumnToContents(0)
        self.tableView.resizeColumnToContents(1)
        self.tableView.setFixedWidth(self.tableView.columnWidth(0) + self.tableView.columnWidth(1))
        self.setMinimumSize(0,600)
        self.adjustSize()
    
    def closeEvent(self, event):
        self.windowClosed.emit()
        event.accept()

class LocationWindow(w.QMainWindow):
    windowClosed = c.pyqtSignal()
    def __init__(self, URL):
        super(LocationWindow, self).__init__()
        self.browser = web.QWebEngineView()
        self.browser.setUrl(c.QUrl(URL))
        self.setCentralWidget(self.browser)
    
    def closeEvent(self, event):
        self.windowClosed.emit()
        event.accept()
    
if __name__ == "__main__":
    a = w.QApplication([])
    a.setApplicationName("EXIF Image Viewer")
    ivw = ImageViewerWindow()
    ivw.openMenuDialog(firstStart = True)
    a.exec()