from PyQt5.QtWidgets import (QMainWindow, QApplication, QGroupBox, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget,
                             QTabWidget, QComboBox, QCheckBox, QListWidget, QDialog, QMessageBox)


class AddTeacherPopUp(QDialog):

    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.name = name
        self.label = QLabel(self.name, self)


class QuitPopUp(QMessageBox):

    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.setIcon(QMessageBox.Warning)
        self.setText("Ohne speichern verlassen?")
        self.setWindowTitle("Exit")
        self.setDetailedText("Es scheint, als wäre etwas verändert worden."
                             "Wird nicht gespeichert, gehen alle Änderungen verloren!\n"
                             "Diese Warnung kann jedoch auch fälschlicherweise angezeigt werden,"
                             "wenn Sie Änderungen manuell rückgängig gemacht werden...")
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.setDefaultButton(QMessageBox.No)

        self.close = None

        returnValue = self.exec()
        if returnValue == QMessageBox.Yes:
            self.close = True
        if returnValue == QMessageBox.No:
            self.close = False


    def get(self):
        return self.close