import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from qt_material import apply_stylesheet
import resources

class SideBar(QWidget):
    def __init__(self, parent=None):
        super(SideBar, self).__init__(parent)
        self.setObjectName('sidebar')
        # create a sidebar on the left with main content on the right
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setObjectName('splitter')
        self.splitter.setHandleWidth(1)
        self.splitter.setChildrenCollapsible(False)
        # set handle border to theme border colour
        self.splitter.setStyleSheet('QSplitter::handle { background-color: %s; }' % self.palette().color(QPalette.Window).name())
        # create a sidebar
        self.sidebar = QWidget()
        self.sidebar.setObjectName('sidebar')
        self.sidebar.setMinimumWidth(200)
        self.sidebar.setMaximumWidth(200)
        # align objects inside sidebar to top
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_layout.setAlignment(Qt.AlignTop)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar.setLayout(self.sidebar_layout)
        # fill to height of parent and remain fixed when scrolling
        self.sidebar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        # create expanding main content
        self.main_content = QWidget()
        self.main_content.setObjectName('main_content')
        self.main_content.setMinimumWidth(200)
        # make main_content expand to fill available space
        self.splitter.addWidget(self.sidebar)
        self.splitter.addWidget(self.main_content)
        # create a layout for the main content
        self.main_content_layout = QVBoxLayout()
        self.main_content_layout.setContentsMargins(0, 0, 0, 0)
        self.main_content_layout.setSpacing(0)
        self.main_content.setLayout(self.main_content_layout)
        # create a layout for the whole widget
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.splitter)
        self.setLayout(self.layout)
    
    def addNavigation(self, title, function, checked=False):
        # create flat button that expands widthwarda
        self.expand_button = QPushButton()
        # expand only widthwards
        self.expand_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # set flat button style
        self.expand_button.setObjectName('expand_button')
        self.expand_button.setFlat(True)
        self.expand_button.setCheckable(True)
        self.expand_button.setChecked(checked)
        self.expand_button.setFixedHeight(40)
        self.expand_button.setStyleSheet('QPushButton#expand_button { background-color: transparent; }')
        self.expand_button.setText(title)

        self.expand_button.clicked.connect(function)
        # add button to sidebar
        self.sidebar_layout.addWidget(self.expand_button)   
    
    def addWidget(self, widget):
        self.main_content_layout.addWidget(widget)


class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle("Python Menus & Toolbars")
        # apply_stylesheet(self, theme='light_blue.xml')
        #self.setStyleSheet("background-color: white;")
        self.resize(600, 480)
        self._createMenuBar()
        self._createToolBars()
        self._createStatusBar()
        self.Page("login")


    def useIcon(self, name):
        if self.systemDarkMode():
            return QIcon(':/icons/' + name + "-dark.svg")
        else:
            return QIcon(':/icons/' + name + '.svg')

    def scrollablePage(self):
        # create scrollable re-usable widget
        layout = QVBoxLayout()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidget(QWidget())
        scroll.widget().setLayout(layout)
        return scroll

    def login(self):
        # if both inputs are empty, show error window saying "Both inputs are empty"    
        if self.username.text() == "" and self.password.text() == "":
            QMessageBox.warning(self, "Error", "Both inputs are empty")
            return
        # if username is empty, show error window saying "Username is empty"
        elif self.username.text() == "":
            QMessageBox.warning(self, "Error", "Username is empty")
            return
        
        # Hide main window and show progressbar window
        self.hide()
        self.progressBar = QProgressDialog("Logging in...", "Cancel", 0, 100, self)
        self.progressBar.setWindowModality(Qt.WindowModal)
        self.progressBar.setWindowTitle("Please wait")
        self.progressBar.setMinimumDuration(0)
        self.progressBar.setValue(0)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setCancelButton(None)
        self.progressBar.show()
        # simulate progress
        for i in range(100):
            if self.progressBar.wasCanceled():
                break
            self.progressBar.setValue(i)
            QApplication.processEvents()
            QThread.msleep(10)
        # hide progressbar window
        self.progressBar.hide()
        # show main window
        self.show()
        self.Page("main")


    def Page(self, id):
        # destroy previous CentralWidget
        if self.centralWidget() is not None:
            self.centralWidget().deleteLater()

        # create new CentralWidget
        scrollablePage = self.scrollablePage()
        if id == "main":
            # create home page
            # show toolbar and menu bar
            self.menuBar().show()
            # show all toolbars
            for toolbar in self.findChildren(QToolBar):
                toolbar.show()
            
            # add sidenav and content
            layout = SideBar()
            layout.addNavigation("Home", lambda: self.Page("home"), checked=True)
            
            # create circle progress bar
            self.progress = QProgressBar()
            self.progress.setRange(0, 100)
            self.progress.setValue(0)
            self.progress.setTextVisible(False)
            self.progress.setFixedWidth(200)
            self.progress.setFixedHeight(200)
            self.progress.setStyleSheet("background-color: " + self.palette().color(QPalette.Highlight).name() + ";")
            self.progress.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.progress)


            scrollablePage.setWidget(layout)
            # add scrollablePage to self
            
            scrollablePage.setWidgetResizable(True)
            scrollablePage.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            self.setCentralWidget(scrollablePage)
            

    def _createMenuBar(self):
        menuBar = self.menuBar()
        # Creating menus using a QMenu object
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        # Creating menus using a title
        editMenu = menuBar.addMenu("&Edit")
        helpMenu = menuBar.addMenu("&Help")

        # Creating actions for menus
        newAction = QAction("&New", self)
        fileMenu.addAction(newAction)
        openAction = QAction("&Open", self)
        fileMenu.addAction(openAction)
        saveAction = QAction("&Save", self)
        fileMenu.addAction(saveAction)
        saveAsAction = QAction("Save &As", self)
        fileMenu.addAction(saveAsAction)
        quitAction = QAction("&Quit", self)
        quitAction.setShortcut("Ctrl+Q")
        fileMenu.addAction(quitAction)
        # connect quitAction to closeEvent
        quitAction.triggered.connect(self.close)

        # set menu to default window menu
        self.setMenuBar(menuBar)

        
    def _createToolBars(self):
        # Using a title
        ToolBar = self.addToolBar("File")
        ToolBar.setMovable(False)


        exitAct = QAction(QIcon(self.useIcon("folder-add")), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        #exitAct.triggered.connect(self.close)
        ToolBar.addAction(exitAct)
    
    def _createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def systemDarkMode(self):
        return self.isDarkMode()

    def isDarkMode(self):
        # QT check if bakcground is dark
        if self.palette().color(QPalette.Background).value() < 128:
            print("Dark mode")
            return True
        else:
            return False


    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
