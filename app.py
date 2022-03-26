from calendar import c
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from qt_material import apply_stylesheet
import resources
import requests

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

    def systemDarkMode(self):
        return self.isDarkMode()

    def isDarkMode(self):
        # QT check if bakcground is dark
        if self.palette().color(QPalette.Background).value() < 128:
            return True
        else:
            return False

    def useIcon(self, name):
        if self.systemDarkMode():
            return QIcon(':/icons/' + name + "-dark.svg")
        else:
            return QIcon(':/icons/' + name + '.svg')
    
    def addNavigation(self, title, function, checked=False, icon=None, colour=None):
        # create flat button that expands widthwarda
        self.expand_button = QPushButton()
        # add icon to left of button
        if icon:
            self.expand_button.setIcon(self.useIcon(icon))

        # expand only widthwards
        self.expand_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # set flat button style
        self.expand_button.setObjectName('expand_button')
        self.expand_button.setFlat(True)
        self.expand_button.setCheckable(True)
        self.expand_button.setChecked(checked)
        self.expand_button.setFixedHeight(30)
        # if background colour of button is bright then use dark text colour
        if self.expand_button.palette().color(QPalette.Background).value() > 128:
            textColour = '#000000'
        else:
            # use theme default text colour
            textColour = '#ffffff'
        # remove border from flat button and if checked, set background colour to theme highlight which is overridden by colour
        if colour:
            self.expand_button.setStyleSheet('QPushButton { margin: 0px; border: none; background-color: %s; color: %s; } QPushButton:checked { background-color: %s; }' % (colour, textColour, colour)) 
        elif checked:
            self.expand_button.setStyleSheet('QPushButton { margin: 0px; border: none; background-color: %s; color: %s; } QPushButton:checked { background-color: %s; }' % (self.palette().color(QPalette.Highlight).name(), textColour, self.palette().color(QPalette.Highlight).name()))            
        else:
            self.expand_button.setStyleSheet('QPushButton { margin: 0px; border: none; background-color: %s; color: %s; }' % (self.palette().color(QPalette.Window).name(), textColour))

        self.expand_button.setText(title)

        self.expand_button.clicked.connect(function)
        # add button to sidebar
        self.sidebar_layout.addWidget(self.expand_button)   
    
    def addNavigationSeparator(self):
        self.sidebar_layout.addWidget(QFrame())

    def addNavigationSpacer(self):
        # add flexible spacer that expands to fill available space in sidebar_layout
        self.sidebar_layout.addStretch()


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
        self.resize(680, 480)
        self._createMenuBar()
        self._createToolBars()
        self._createStatusBar()
        self.Page("main")

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

    def pageIsOn(self, page):
        if self.currentPage == page:
            return True
        else:
            return False 

    def Page(self, id):
        self.currentPage = id
        # destroy previous CentralWidget
        if self.centralWidget() is not None:
            self.centralWidget().deleteLater()

        layout = SideBar()

        layout.addNavigation("Home", lambda: self.Page("main"), checked=self.pageIsOn("main"))
        layout.addNavigationSpacer()
        layout.addNavigation("Updates", lambda: self.Page("settings"), checked=self.pageIsOn("settings"), icon="update-none", colour="#FFA000")
        # amber colour in hex
        layout.addNavigation("Settings", lambda: self.Page("settings"), checked=self.pageIsOn("settings"))
        # create new CentralWidget
        scrollablePage = self.scrollablePage()
        if id == "main":
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
        
        if id == "plasmoid":
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
        
        if id == "apps":
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


        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
