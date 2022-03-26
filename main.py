# load and run app.py and on error, display error message using pyqt5
import app
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from qt_material import apply_stylesheet
import resources
import traceback
import webbrowser

def sendIssue(title, body):
    # copy body to clipboard
    clipboard = QApplication.clipboard()
    clipboard.setText(body)
    # open browser to https://github.com/StringentDev/Quarternion/issues/new
    url = 'https://github.com/StringentDev/Quarternion/issues'
    # open default browser at url
    webbrowser.open(url)
    

if __name__ == "__main__":
    try:
        root = QApplication(sys.argv)
        win = Window()
        win.show()
        sys.exit(root.exec_())
    except Exception as e:
        # display verbose error message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error: " + str(e))
        msg.setInformativeText("Do you want to report this issue to the developer?.")
        msg.setWindowTitle("Error")
        # set detailed message to error message stack trace
        msg.setDetailedText(traceback.format_exc())
        # send github issue button
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.buttonClicked.connect(lambda x: sendIssue(str(e), traceback.format_exc()))
        # show message box
        msg.exec_()
